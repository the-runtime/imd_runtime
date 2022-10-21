import asyncio

import scrape

async def main():

    tasks = []

    i = 1000

    j = 0

    while j < 140:
        url = "https://www.imdb.com/search/title/?release_date=2018-01-01,2018-12-31&sort=num_votes,desc&start="+str(i)+"&ref_=adv_nxt"
        i = i+50
        tasks.append(asyncio.ensure_future(scrape.scrape(url)))
        j=j+1
    data_list = await asyncio.gather(*tasks)

    largest = data_list[0]
    print("-----------------finally------------")
    for r in data_list:
        if r[2] > largest[2]:
            largest = r
    

    print(largest)


if __name__=="__main__":
    asyncio.run(main())
