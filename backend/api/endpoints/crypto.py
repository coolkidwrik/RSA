import asyncio
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from api.dependencies import AppState, get_app_state, get_rsa_crypto
from core.rsa_crypto import RSACrypto
from models.crypto_models import RSAKeyPair
from models.schemas import (
    BlockInfo,
    DecryptionRequest,
    DecryptionResponse,
    EncryptionRequest,
    EncryptionResponse,
)

router = APIRouter(prefix="/crypto", tags=["Encryption & Decryption"])


@router.post("/encrypt", response_model=EncryptionResponse)
async def encrypt_message(
    request: EncryptionRequest, rsa_crypto: RSACrypto = Depends(get_rsa_crypto)
):
    """
    Encrypt a message using RSA public key.

    The message is automatically split into blocks that fit within the key size.
    """
    try:
        # Convert string keys to integers
        n = int(request.n)
        e = int(request.e)

        # Perform encryption in thread pool
        loop = asyncio.get_event_loop()
        crypto_result = await loop.run_in_executor(
            None, rsa_crypto.encrypt_message, request.message, n, e
        )

        if not crypto_result.success:
            raise HTTPException(
                status_code=400, detail=crypto_result.error_message or "Encryption failed"
            )

        # Convert blocks to response format
        encrypted_blocks = [str(block.encrypted_value) for block in crypto_result.blocks]
        block_info = [
            BlockInfo(
                block_number=block.block_number,
                original_value=str(block.original_value),
                encrypted_value=str(block.encrypted_value),
                original_hex=block.original_hex,
                encrypted_hex=block.encrypted_hex,
            )
            for block in crypto_result.blocks
        ]

        return EncryptionResponse(
            encrypted_blocks=encrypted_blocks,
            block_info=block_info,
            total_blocks=len(encrypted_blocks),
            message_length=len(request.message),
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Encryption failed: {str(e)}")


@router.post("/decrypt", response_model=DecryptionResponse)
async def decrypt_message(
    request: DecryptionRequest, rsa_crypto: RSACrypto = Depends(get_rsa_crypto)
):
    """
    Decrypt a message using RSA private key.

    Takes encrypted blocks and reconstructs the original message.
    """
    try:
        # Convert string keys to integers
        n = int(request.n)
        d = int(request.d)
        encrypted_blocks = [int(block) for block in request.encrypted_blocks]

        # Perform decryption in thread pool
        loop = asyncio.get_event_loop()
        crypto_result = await loop.run_in_executor(
            None, rsa_crypto.decrypt_message, encrypted_blocks, n, d
        )

        if not crypto_result.success:
            raise HTTPException(
                status_code=400, detail=crypto_result.error_message or "Decryption failed"
            )

        return DecryptionResponse(
            decrypted_message=crypto_result.message,
            success=True,
            block_count=len(crypto_result.blocks),
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Decryption failed: {str(e)}")


@router.post("/encrypt-with-stored-keys")
async def encrypt_with_stored_keys(
    message: str,
    state: AppState = Depends(get_app_state),
    rsa_crypto: RSACrypto = Depends(get_rsa_crypto),
):
    """
    Encrypt a message using the currently stored public key.
    Convenience endpoint that doesn't require passing keys explicitly.
    """
    if state.current_keypair is None:
        raise HTTPException(status_code=400, detail="No keys available. Generate keys first.")

    request = EncryptionRequest(
        message=message, n=str(state.current_keypair.n), e=str(state.current_keypair.e)
    )

    return await encrypt_message(request, rsa_crypto)


@router.post("/decrypt-with-stored-keys")
async def decrypt_with_stored_keys(
    encrypted_blocks: List[str],
    state: AppState = Depends(get_app_state),
    rsa_crypto: RSACrypto = Depends(get_rsa_crypto),
):
    """
    Decrypt blocks using the currently stored private key.
    Convenience endpoint that doesn't require passing keys explicitly.
    """
    if state.current_keypair is None:
        raise HTTPException(status_code=400, detail="No keys available. Generate keys first.")

    request = DecryptionRequest(
        encrypted_blocks=encrypted_blocks,
        n=str(state.current_keypair.n),
        d=str(state.current_keypair.d),
    )

    return await decrypt_message(request, rsa_crypto)
