import asyncio
import urllib.parse

import aiohttp
from flask import (Flask, make_response, redirect, render_template, request,
                   url_for)

app = Flask(__name__)

ulcs = [
    "EECS 367",
    "EECS 373",
    "EECS 388",
    "EECS 390",
    "EECS 427",
    "EECS 442",
    "EECS 445",
    "EECS 470",
    "EECS 471",
    "EECS 475",
    "EECS 476",
    "EECS 477",
    "EECS 478",
    "EECS 481",
    "EECS 482",
    "EECS 483",
    "EECS 484",
    "EECS 485",
    "EECS 486",
    "EECS 487",
    "EECS 489",
    "EECS 490",
    "EECS 491",
    "EECS 492",
    "EECS 493",
]

capstones = [
    "EECS 440",
    "EECS 441",
    "EECS 448",
    "EECS 449",
    "EECS 467",
    "EECS 470",
    "EECS 473",
    "EECS 480",
    "EECS 494",
    "EECS 495",
    "EECS 497",
]

flex_tech = [
    "EECS 201",
    "EECS 270",
    "EECS 285",
    "EECS 440",
    "EECS 441",
    "EECS 448",
    "EECS 449",
    "EECS 467",
    "EECS 473",
    "EECS 480",
    "EECS 494",
    "EECS 495",
    "EECS 497",
    "EECS 543",
    "EECS 545",
    "EECS 547",
    "EECS 567",
    "EECS 568",
    "EECS 570",
    "EECS 571",
    "EECS 573",
    "EECS 574",
    "EECS 575",
    "EECS 576",
    "EECS 578",
    "EECS 579",
    "EECS 582",
    "EECS 583",
    "EECS 584",
    "EECS 586",
    "EECS 587",
    "EECS 588",
    "EECS 589",
    "EECS 590",
    "EECS 591",
    "EECS 592",
    "EECS 595",
]


async def get(url, session):
    try:
        async with session.get(url=url) as response:
            j = await response.json()
            print("Successfully got url {}".format(url))
            return j
    except Exception as e:
        print("Unable to get url {} due to {}.".format(url, e))


async def get_classes(urls, sessionid):
    async with aiohttp.ClientSession(
        cookies={"sessionid": sessionid}
    ) as session:
        ret = await asyncio.gather(*[get(url, session) for url in urls])
    print("Finalized all. Return is a list of len {} outputs.".format(len(ret)))
    return ret


@app.route("/error/")
def error():
    return render_template("error.html")


@app.route("/auth/", methods=("GET", "POST"))
def auth():
    if request.method == "POST":
        sessionid = request.form["sessionid"]
        resp = make_response(redirect(url_for("index")))
        resp.set_cookie("sessionid", sessionid)
        return resp
    resp = make_response(render_template("auth.html"))
    resp.set_cookie("sessionid", "")
    return resp


@app.route("/")
async def index():
    if (
        request.cookies.get("sessionid") is None
        or request.cookies.get("sessionid") == ""
    ):
        return redirect(url_for("auth"))

    sessionid = request.cookies.get("sessionid")
    print("sessionid: {}".format(sessionid))

    api_urls = [
        "https://atlas.ai.umich.edu/api/section-table-data/{}/".format(
            urllib.parse.quote(c)
        )
        for c in ulcs
    ]

    # parse jsons
    info = []

    try:
        jsons_list = await get_classes(api_urls, sessionid)

        print("Got classes succesfully.")

        for j in jsons_list:
            lecture_open = 0
            lecture_wait = 0
            open_seats = 0
            waitlist_size = 0
            for section in j["sections"]:
                if section["SectionType"] != "LEC":
                    open_seats += section["AvailableSeats"]
                    waitlist_size += section["WaitTotal"]
                else:
                    lecture_open += section["AvailableSeats"]
                    lecture_wait += section["WaitTotal"]

            if len(j["extra_data"]) == 0:
                print(f"unable to add: {j}")
                continue

            abbreviation = j["extra_data"][0]["course_code"]
            name = j["extra_data"][0]["title"]

            link = "https://atlas.ai.umich.edu/course/{}/".format(
                urllib.parse.quote(
                    j["extra_data"][0]["subject_id"]
                    + " "
                    + j["extra_data"][0]["catalog_number"]
                )
            )

            if open_seats == 0 and waitlist_size == 0:
                open_seats = lecture_open
                waitlist_size = lecture_wait

            open_seats = min(open_seats, lecture_open)
            waitlist_size = min(waitlist_size, lecture_wait)

            info.append(
                {
                    "link": link,
                    "name": name,
                    "abbrev": abbreviation,
                    "status": "open" if open_seats > 0 else "closed",
                    "number": open_seats if open_seats > 0 else waitlist_size,
                }
            )

    except Exception as e:
        print(f"unsuccessful get classes. {e}")
        return redirect(url_for("error"))

    return render_template("index.html", data=info)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
