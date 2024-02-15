def setup_routes(app, handler):
    router = app.router
    router.add_get('/', handler.get_root)
    router.add_get('/cities', handler.get_cities)
    router.add_get('/cities/{name}', handler.get_city)
    router.add_post('/cities/{name}', handler.add_city)
    router.add_delete('/cities/{name}', handler.delete_city)
    router.add_get('/resolver', handler.resolve_coordinates)
