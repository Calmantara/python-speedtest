import speedtest
import time
import datetime
import schedule

bit_to_megabyte = 1048576  # to convert bit into mega byte
schedule_time = 0.1  # schedule time in minutes
#seoul, bandung, jakarta, bangkok, singapore, china
# ,[7580], [23158], [17760], [2054], [3633], [10567]]
servers_list = [[6527], [2054]]


def test(servers: list):
    s = speedtest.Speedtest()
    s.get_servers(servers)
    s.download()
    s.upload()
    res = s.results.dict()

    ts = datetime.datetime.now().timestamp()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    return res["download"], res["upload"], res["ping"], res["server"]["country"], st


# This is comment for empty list


def get_data():
    # write to csv
    for i in range(len(servers_list)):
        global first_run_list
        try:
            temp = first_run_list[i]
        except:
            first_run_list.append(0)
        with open('{}.csv'.format(servers_list[i][0]), 'a') as f:
            if(first_run_list[i] == 0):
                f.write('download,upload,ping,country,timestamp\n')
                first_run_list[i] = 1
                d, u, p, c, t = test(servers=servers_list[i])
                f.write('{},{},{},{},{}\n'.format(
                    (d/bit_to_megabyte), (u/bit_to_megabyte), p, c, t))
                print("Data was successfully saved in {}.csv!".format(
                    servers_list[i][0]))


schedule.every(schedule_time).minutes.do(get_data)


def main():
    # This is main procedure
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
