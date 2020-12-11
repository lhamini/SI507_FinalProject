from flask import Flask, render_template, request
import query
import search
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

# @app.route('/searchbox', methods=['POST', 'GET'])
# def searchbox():
#     return render_template('search.html')

@app.route('/searchbox')
def results():
    return render_template('search.html')

@app.route('/searchbox', methods=['POST'])
def process_res():
    user_search_query = request.form['msg']
    corpus, ranking_function, cache_dict= search.corpus_index()
    date_list = list(cache_dict.keys())
    summary_list = list(cache_dict.values())
    tokenized_query = search.remove_stopwords(user_search_query.lower().split(" "))
    response = ranking_function.get_top_n(tokenized_query, corpus, n=10)
    return render_template('search.html', search_results_list = response,
                                          user_query=user_search_query,
                                          date_list=date_list,
                                          summary_list=summary_list)


@app.route('/<date>')
def crash_details(date):
    crash_details = query.crash_details_query(date)
    return render_template('crash_info.html', crash_details=crash_details)




if __name__ == "__main__":
    app.run(debug=True)
