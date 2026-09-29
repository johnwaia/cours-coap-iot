"""Télécharge /biglog bloc par bloc (option Block2) avec une taille imposée.
Usage : python blockwise.py 256   (tailles valides : 16, 32, ..., 1024)"""
import asyncio
import sys
import aiocoap
from aiocoap.optiontypes import BlockOption


async def main(taille):
    szx = taille.bit_length() - 5          # 16 -> 0, 32 -> 1, ..., 1024 -> 6
    ctx = await aiocoap.Context.create_client_context()
    donnees, num, encore = b"", 0, True
    while encore:
        req = aiocoap.Message(code=aiocoap.Code.GET, uri="coap://localhost/biglog")
        req.opt.block2 = BlockOption.BlockwiseTuple(num, False, szx)
        rep = await ctx.request(req, handle_blockwise=False).response
        b = rep.opt.block2
        print(f"bloc {b.block_number:3d} : {len(rep.payload):4d} octets, more={b.more}")
        donnees += rep.payload
        num, encore = b.block_number + 1, b.more
    print(f"=> {num} blocs de {taille} octets, total {len(donnees)} octets")
    await ctx.shutdown()


if __name__ == "__main__":
    asyncio.run(main(int(sys.argv[1]) if len(sys.argv) > 1 else 256))
