from flask import Flask, render_template, request
import query
app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html', year_list = query.crash_year_list())

@app.route('/statistics', methods=['POST'])
def statistics():
    year = request.form['year']
    sort = request.form['sort']
    show_results = request.form['show_results']
    crashes_for_each_year = query.crashes_for_each_year(year, sort)
    agg_for_each_year = query.agg_for_each_year(year)
    map_for_each_year_div = query.plot_map(year, sort)
    bar_for_each_year_div = query.plot_bar(year, sort)
    return render_template('statistics.html',
                                year=year,
                                crashes_for_each_year=crashes_for_each_year,
                                agg_for_each_year=agg_for_each_year,
                                show_results=show_results,
                                map_for_each_year_div=map_for_each_year_div,
                                bar_for_each_year_div=bar_for_each_year_div)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/<date>')
def crash_details(date):
    crash_details = query.crash_details_query(date)
    return render_template('crash_info.html', crash_details=crash_details)


if __name__ == "__main__":
    app.run(debug=True)
