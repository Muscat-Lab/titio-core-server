import argparse
import logging

import uvicorn

if __name__ == '__main__':
    parse = argparse.ArgumentParser()

    parse.add_argument("--host", type=str, default="0.0.0.0")
    parse.add_argument("--port", type=int, default=9900)
    parse.add_argument("--reload", type=bool, default=True)

    args = parse.parse_args()

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("uvicorn").setLevel(logging.DEBUG)
    logging.info(f"Server is running on {args.host}:{args.port}")

    uvicorn.run("src.main:app", host=args.host, port=args.port, reload=args.reload)
