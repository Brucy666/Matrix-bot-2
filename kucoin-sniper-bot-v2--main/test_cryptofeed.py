from cryptofeed import FeedHandler
from cryptofeed.exchanges import Binance
from cryptofeed.defines import TRADES, L2_BOOK


# ✅ Must be async and accept 2 arguments
async def trade_callback(trade, receipt_timestamp):
    print(f"✅ Trade @ {receipt_timestamp}: {trade}")


async def book_callback(book, receipt_timestamp):
    print(f"📘 Book Update @ {receipt_timestamp}: {book}")


def main():
    fh = FeedHandler()
    fh.add_feed(Binance(
        symbols=['BTC-USDT'],
        channels=[TRADES, L2_BOOK],
        callbacks={
            TRADES: trade_callback,
            L2_BOOK: book_callback
        }
    ))
    fh.run()


if __name__ == "__main__":
    main()
