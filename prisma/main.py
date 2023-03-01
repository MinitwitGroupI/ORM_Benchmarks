import asyncio
from prisma import Prisma

""" ('''
                select messages.*, users.* from messages, users
                where messages.flagged = 0 and messages.author_id = users.user_id and (
                    users.user_id = %s or
                    users.user_id in (select whom_id from followers
                                            where who_id = %s))
                order by messages.pub_date desc limit %s''',
                [user_id, user_id, per_page_limit])
    """

user_id = 1
per_page_limit = 10

async def main() -> None:
    prisma = Prisma()
    await prisma.connect()

    result = prisma.messages.find_many(
    where={
        'flagged': False,
        'author': {
            'users': {
                'OR': [
                    {'user_id': user_id},
                    {'followers': {'some': {'who_id': user_id}}},
                ]
            }
        }
    },
    order_by=[{'pub_date': 'desc'}],
    take=per_page_limit,
    include={'author': True}
)

    # await prisma.disconnect()

if __name__ == '__main__':
    asyncio.run(main())