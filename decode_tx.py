def decode_varint(hex_str):
    """Decode a variable-length integer from hex string. Returns (value, bytes_consumed)."""
    data = bytes.fromhex(hex_str)
    first = data[0]
    if first < 0xfd:
        return first, 1
    elif first == 0xfd:
        return int.from_bytes(data[1:3], 'little'), 3
    elif first == 0xfe:
        return int.from_bytes(data[1:5], 'little'), 5
    else:
        return int.from_bytes(data[1:9], 'little'), 9

def decode_tx(tx_hex):
    tx_bytes = bytes.fromhex(tx_hex)
    offset = 0

    # Version (4 bytes, little-endian)
    version = int.from_bytes(tx_bytes[offset:offset+4], 'little')
    offset += 4
    print(f"\nVersion: {version}")

    # Check for SegWit marker & flag
    is_segwit = False
    if tx_bytes[offset] == 0x00 and tx_bytes[offset+1] == 0x01:
        is_segwit = True
        offset += 2
        print("SegWit transaction\n")

    # Input Count (varint)
    input_count_hex = tx_hex[offset*2:]  # hex string from offset
    input_count, varint_size = decode_varint(input_count_hex)
    offset += varint_size
    print(f"Input Count: {input_count}")

    # Inputs
    for i in range(input_count):
        # txid (32 bytes, reversed)
        txid_bytes = tx_bytes[offset:offset+32]
        txid = txid_bytes[::-1].hex()
        offset += 32
        # vout (4 bytes)
        vout = int.from_bytes(tx_bytes[offset:offset+4], 'little')
        offset += 4
        # scriptSig length (varint)
        script_len_hex = tx_hex[offset*2:]
        script_len, varint_size2 = decode_varint(script_len_hex)
        offset += varint_size2
        # scriptSig (skip content for now)
        offset += script_len
        # sequence (4 bytes)
        sequence = int.from_bytes(tx_bytes[offset:offset+4], 'little')
        offset += 4
        print(f"Input {i}: txid={txid}, vout={vout}, sequence={hex(sequence)}")

    # Output Count
    output_count_hex = tx_hex[offset*2:]
    output_count, varint_size = decode_varint(output_count_hex)
    offset += varint_size
    print(f"\nOutput Count: {output_count}")

    # Outputs
    for i in range(output_count):
        # amount (8 bytes, little-endian, in satoshis)
        amount = int.from_bytes(tx_bytes[offset:offset+8], 'little')
        offset += 8
        # scriptPubKey length (varint)
        pk_script_len_hex = tx_hex[offset*2:]
        pk_script_len, varint_size2 = decode_varint(pk_script_len_hex)
        offset += varint_size2
        # scriptPubKey
        script_pubkey = tx_bytes[offset:offset+pk_script_len].hex()
        offset += pk_script_len
        print(f"Output {i}: {amount} satoshis, scriptPubKey={script_pubkey}")

    # Skip witness and locktime for simplicity in manual decode
    

    print("\nDecoding complete!\n \n")

# Transaction hex
tx_hex = "0200000000010131811cd355c357e0e01437d9bcf690df824e9ff785012b6115dfae3d8e8b36c10100000000fdffffff0220a107000000000016001485d78eb795bd9c8a21afefc8b6fdaedf718368094c08100000000000160014840ab165c9c2555d4a31b9208ad806f89d2535e20247304402207bce86d430b58bb6b79e8c1bbecdf67a530eff3bc61581a1399e0b28a741c0ee0220303d5ce926c60bf15577f2e407f28a2ef8fe8453abd4048b716e97dbb1e3a85c01210260828bc77486a55e3bc6032ccbeda915d9494eda17b4a54dbe3b24506d40e4ff43030e00"

decode_tx(tx_hex)
