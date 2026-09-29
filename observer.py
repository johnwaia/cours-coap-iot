"""Client d'observation : s'abonne à /temp et affiche les notifications
pendant N secondes (par défaut 10)."""
import asyncio
import sys
import aiocoap


async def main(duree):
    ctx = await aiocoap.Context.create_client_context()
    req = aiocoap.Message(code=aiocoap.Code.GET, uri="coap://localhost/temp",
                          observe=0)
    demande = ctx.request(req)
    rep = await demande.response
    print(f"réponse initiale : {rep.code} {rep.payload.decode()} (Observe={rep.opt.observe})")
    n = 0

    async def notifications():
        nonlocal n
        async for notif in demande.observation:
            n += 1
            print(f"notification {n} : {notif.payload.decode()} (Observe={notif.opt.observe})")

    try:
        await asyncio.wait_for(notifications(), duree)
    except asyncio.TimeoutError:
        pass
    demande.observation.cancel()
    print(f"=> {n} notifications en {duree} s")
    await ctx.shutdown()


if __name__ == "__main__":
    asyncio.run(main(float(sys.argv[1]) if len(sys.argv) > 1 else 10))
