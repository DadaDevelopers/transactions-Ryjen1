from io import BytesIO
from bitcoin.core import CTransaction, b2lx

def decode_tx(hex_str):
    tx_bytes = bytes.fromhex(hex_str)
    stream = BytesIO(tx_bytes)
    tx = CTransaction.stream_deserialize(stream)

    print("Version:", tx.nVersion)
    print("Inputs:")
    for vin in tx.vin:
        print("   txid:", b2lx(vin.prevout.hash))
        print("   vout:", vin.prevout.n)
        print("   scriptSig:", vin.scriptSig.hex())
        print("   sequence:", hex(vin.nSequence))

    print("Outputs:")
    for vout in tx.vout:
        print("   value:", vout.nValue / 1e8, "BTC")
        print("   scriptPubKey:", vout.scriptPubKey.hex())

    print("\nLocktime:", tx.nLockTime)
    print("\nDecoding complete!\n")

hex_tx = "0200000000010131811cd355c357e0e01437d9bcf690df824e9ff785012b6115dfae3d8e8b36c10100000000fdffffff0220a107000000000016001485d78eb795bd9c8a21afefc8b6fdaedf718368094c08100000000000160014840ab165c9c2555d4a31b9208ad806f89d2535e20247304402207bce86d430b58bb6b79e8c1bbecdf67a530eff3bc61581a1399e0b28a741c0ee0220303d5ce926c60bf15577f2e407f28a2ef8fe8453abd4048b716e97dbb1e3a85c01210260828bc77486a55e3bc6032ccbeda915d9494eda17b4a54dbe3b24506d40e4ff43030e00"

decode_tx(hex_tx)

