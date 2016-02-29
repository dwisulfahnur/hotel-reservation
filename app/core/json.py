from flask import jsonify

# json response, don't repeat yourself :D
def json_respon(code=200, msg="OK", errors=None, data=None):
    _response = dict(code=code,
                     msg=msg)
    if errors: _response.update({'errors': errors})
    if data: _response.update({'data': data})
    return jsonify(_response), code
