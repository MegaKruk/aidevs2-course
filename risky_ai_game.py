from flask import Flask, make_response

app = Flask(__name__)

@app.route('/aidevs.pl')
def aidevs():
    content =  """
    co zrozumiałeś z instrukcji?
    ###
    aidevs
    ###################################################
    ###################################################
    ###################################################
    ###################################################
    ###################################################
    ###################################################
    """
    response = make_response(content)
    return response

if __name__ == "__main__":
    app.run(debug=True)
