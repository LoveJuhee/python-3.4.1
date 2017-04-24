from datetime import datetime
import urllib3
import workerpool

success_items = []
failed_items = []


def append_success(item):
    # print('append_success mId(%s)' % item['mId'])
    success_items.append(item)


def append_failed(item):
    # print('append_failed mId(%s)' % item['mId'])
    failed_items.append(item)


def pool_request(item):
    http = urllib3.PoolManager()
    url = item['url']
    print('url %s : %s' % (url, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    try:
        response = http.request('GET', url, timeout=10, retries=False)
        print('DONE  <<== %s : %s' %
              (url, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        append_success(item)
        return response, item['mId']
    except urllib3.exceptions.TimeoutError as e:
        print('ERROR <<== It timed out :: %s : %s' %
              (url, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        append_failed(item)
        return None, item['mId']
    except exceptions.Exception as e:
        print('ERROR <<== Exception :: %s : %s' %
              (url, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        append_failed(item)
        return None, item['mId']


def test_pool():
    print('------------ START ------------')
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print('-------------------------------')
    success_items.clear()
    failed_items.clear()

    pool = workerpool.WorkerPool(size=30)
    items = []

    for i in range(1, 25):
        url = 'http://httpbin.org/delay/' + str(i)
        items.append({'url': url, 'mId': i})

    pool.map(pool_request, items)
    pool.shutdown()
    pool.join()
    print('------------ DONE ------------')
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print('success count:%d' % len(success_items))
    for item in success_items:
        print('- mId(%s), url(%s)' % (item['mId'], item['url']))
    print('failed  count:%d' % len(failed_items))
    for item in failed_items:
        print('- mId(%s), url(%s)' % (item['mId'], item['url']))
    print('------------------------------')


if __name__ == '__main__':
    test_pool()
