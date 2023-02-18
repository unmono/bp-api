from fastapi import FastAPI


app = FastAPI()


@app.get('/sections')
async def sections():
    return {'Content': 'List of subsubsections links organized in section-subsection-subsubsection map'}


@app.get('/sections/{subsub_id}')
async def sections(subsub_id: int):
    return {'Content': f'List of products under subsection {subsub_id}.'}


@app.get('/search/{search_query}')
async def sections(search_query: str):
    return {'Content': f'List of products that match the query {search_query}. '
                       f'If there is a single such product, than dirrectly its page.'}


@app.get('/product/{part_number}')
async def sections(part_number: str):
    return {'Content': f'{part_number} product page.'}
