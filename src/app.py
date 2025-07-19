from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def read_root():
    return {'message': 'Hello, World!'}


@app.get('/inexistente')
def read_inexistente():
    return {'detail': 'Not Found'}, 404


@app.post('/')
def post_root():
    return {'detail': 'Method Not Allowed'}, 405


@app.exception_handler(404)
def not_found_exception_handler(request, exc):
    return {'detail': 'Not Found'}, 404


@app.exception_handler(405)
def method_not_allowed_exception_handler(request, exc):
    return {'detail': 'Method Not Allowed'}, 405
