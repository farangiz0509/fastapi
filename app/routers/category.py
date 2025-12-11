from fastapi.routing import APIRouter

router = APIRouter()


@router.get('/')
def get_categories():
    return {'message': 'ok'}
    
@router.get('/list')
def get_list():
    return {'message': 'hi'}
