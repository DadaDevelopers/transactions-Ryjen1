from io import BytesIO
from bitcoin.core import CTransaction, b2lx

def decode_transaction(tx_hex):
    """Decode a Bitcoin transaction from hex string using python-bitcoinlib."""
    tx_bytes = bytes.fromhex(tx_hex)
    stream = BytesIO(tx_bytes)
    tx = CTransaction.stream_deserialize(stream)
    
    print("=" * 50)
    print("DECODED BITCOIN TRANSACTION")
    print("=" * 50)
    print(f"Version: {tx.nVersion}")
    print(f"Locktime: {tx.nLockTime}")
    print(f"Input Count: {len(tx.vin)}")
    
    for i, vin in enumerate(tx.vin):
        txid = b2lx(vin.prevout.hash)
        vout = vin.prevout.n
        script_sig = vin.scriptSig.hex() if vin.scriptSig else "(empty)"
        sequence = hex(vin.nSequence)
        print(f"\n  → Input {i}:")
        print(f"    TXID:     {txid}")
        print(f"    Vout:     {vout}")
        print(f"    ScriptSig: {script_sig}")
        print(f"    Sequence: {sequence}")
    
    print(f"\nOutput Count: {len(tx.vout)}")
    for i, vout in enumerate(tx.vout):
        value_btc = vout.nValue / 100_000_000
        script_pubkey = vout.scriptPubKey.hex()
        print(f"\n  → Output {i}:")
        print(f"    Amount:   {value_btc:.8f} BTC ({vout.nValue} satoshis)")
        print(f"    Script:   {script_pubkey}")

# Given transaction hex
tx_hex = "0200000000010131811cd355c357e0e01437d9bcf690df824e9ff785012b6115dfae3d8e8b36c10100000000fdffffff0220a107000000000016001485d78eb795bd9c8a21afefc8b6fdaedf718368094c08100000000000160014840ab165c9c2555d4a31b9208ad806f89d2535e20247304402207bce86d430b58bb6b79e8c1bbecdf67a530eff3bc61581a1399e0b28a741c0ee0220303d5ce926c60bf15577f2e407f28a2ef8fe8453abd4048b716e97dbb1e3a85c01210260828bc77486a55e3bc6032ccbeda915d9494eda17b4a54dbe3b24506d40e4ff43030e00"

# Run decoder
decode_transaction(tx_hex)
