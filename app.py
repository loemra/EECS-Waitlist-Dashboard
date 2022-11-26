from flask import Flask, render_template, request, redirect, url_for, make_response
import asyncio
import aiohttp
import urllib.parse

app = Flask(__name__)

ulcs = [
    'EECS 373',
    'EECS 388',
    'EECS 390',
    'EECS 427',
    'EECS 442',
    'EECS 445',
    'EECS 470',
    'EECS 475',
    'EECS 477',
    'EECS 481',
    'EECS 482',
    'EECS 483',
    'EECS 484',
    'EECS 485',
    'EECS 486',
    'EECS 487',
    'EECS 489',
    'EECS 490',
    'EECS 492',
    'EECS 493'
]

async def get(url, session):
    try:
        async with session.get(url=url) as response:
            j = await response.json()
            print("Successfully got url {}".format(url))
            return j
    except Exception as e:
        print("Unable to get url {} due to {}.".format(url, e.__class__))

async def get_classes(urls, sessionid):
    async with aiohttp.ClientSession(cookies={'sessionid': sessionid}) as session:
        ret = await asyncio.gather(*[get(url, session) for url in urls])
    print("Finalized all. Return is a list of len {} outputs.".format(len(ret)))
    return ret

@app.route('/error/')
def error():
    return render_template('error.html')

@app.route('/auth/', methods=('GET', 'POST'))
def auth():
    if request.method == 'POST':
        sessionid = request.form['sessionid']
        resp = make_response(redirect(url_for('index')))
        resp.set_cookie('sessionid', sessionid)
        return resp
    resp = make_response(render_template('auth.html'))
    resp.set_cookie('sessionid', '')
    return resp

@app.route('/')
async def index():
    if request.cookies.get('sessionid') is None or request.cookies.get('sessionid') == '':
        return redirect(url_for('auth'))

    sessionid = request.cookies.get('sessionid')
    print('sessionid: {}'.format(sessionid))
    
    api_urls = ['https://atlas.ai.umich.edu/api/section-table-data/{}/'.format(urllib.parse.quote(c)) for c in ulcs]

    # parse jsons
    info = []

    try:
        jsons_list = await get_classes(api_urls, sessionid)

        for j in jsons_list:
            lecture_open = 0
            lecture_wait = 0
            open_seats = 0
            waitlist_size = 0
            for section in j['sections']:
                if section['SectionType'] != 'LEC':
                    open_seats += section['AvailableSeats']
                    waitlist_size += section['WaitTotal']
                else:
                    lecture_open += section['AvailableSeats']
                    lecture_wait += section['WaitTotal']
            abbreviation = j['extra_data'][0]['course_code']
            name = j['extra_data'][0]['title']

            link = 'https://atlas.ai.umich.edu/course/{}/'.format(urllib.parse.quote(j['extra_data'][0]['subject_id'] + ' ' + j['extra_data'][0]['catalog_number']))
            
            if open_seats == 0 and waitlist_size == 0:
                open_seats = lecture_open
                waitlist_size = lecture_wait

            open_seats = min(open_seats, lecture_open)
            waitlist_size = min(waitlist_size, lecture_wait)
            
            info.append({'link': link, 'name': name, 'abbrev': abbreviation, 'status': 'open' if open_seats > 0 else 'closed', 'number': open_seats if open_seats > 0 else waitlist_size})
    except:
        return redirect(url_for('error'))

    return render_template('index.html', data=info)


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8000,debug=True)