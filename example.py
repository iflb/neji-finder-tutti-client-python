import sys
import asyncio

from neji_finder_tutti_client.main import NejiFinderTuttiClient

async def on_response(data):
    print('Data received! (watch_id: {})'.format(data['last_watch_id']))
    print(data)

async def on_error(msg):
    print('on_error', msg)

async def main():
    mode = sys.argv[1]

    client = NejiFinderTuttiClient()

    try:
        await client.open(
                works_host='https://dev.neji-finder.tutti.works',
                market_host='https://dev.neji-finder.tutti.market'
            )
        await client.sign_in(
                works_params={ 'user_name': 'admin', 'password': 'admin' },
                market_params={ 'user_id': 'requester1', 'password': 'requester1' }
            )

        if mode == 'publish':
            automation_parameter_set_id = sys.argv[2]
            if len(sys.argv) < 4:
                print('Usage:  python example.py publish <automation_parameter_set_id>')
                print('')
            else:
                sync_id = sys.argv[3]
                ngid, jid = await client.publish_tasks_to_market(
                        automation_parameter_set_id,
                        sync_id
                    )

        elif mode == 'watch_response':
            if len(sys.argv) < 3:
                print('Usage:  python example.py watch_response <automation_parameter_set_id> <last_watch_id>')
                print('')
            else:
                automation_parameter_set_id = sys.argv[2]
                last_watch_id = sys.argv[3] if len(sys.argv) == 4 else '+'
                print('Started watching response...')
                await client.watch_responses_for_tasks(
                        automation_parameter_set_id,
                        handler = on_response,
                        last_watch_id = last_watch_id
                    )

        elif mode == 'test_connection':
            print('open and sign_in finished')

    except Exception as e:
        print(e.resource, e.err.state, e.err.source)


if __name__=='__main__':
    if len(sys.argv)==1:
        print('Usage:  python example.py <mode> <automation_parameter_set_id> <sync_id>')
        print('Available modes ... "publish", "watch_response"')
        print('')
    else:
        loop = asyncio.get_event_loop()
        loop.create_task(main())
        loop.run_forever()
