import re
import requests

class apicalypse():
    def __init__(self, opts):
        self.apicalypse = opts.get('apicalypse')

        self.config = { 'query_method': 'body' }
        self.config.update(opts)

        self.filter_array = []
    
    def fields(self, fields):
        if fields:
            field_str = ','.join(fields) if isinstance(fields, list) else fields
            field_str = re.sub(r'\s+', '', field_str) if field_str else ''
            self.filter_array.append(f'fields {field_str}')
        return self
    
    def sort(self, field, direction):
        if field:
            self.filter_array.append(f'sort {field} {direction or "asc"}')
        return self
    
    def limit(self, limit):
        if limit:
            self.filter_array.append(f'limit {limit}')
        return self
    
    def offset(self, offset):
        if offset:
            self.filter_array.append(f'offset {offset}')
        return self
    
    def search(self, search):
        if search:
            self.filter_array.append(f'search {search}')
        return self
    
    def filter(self, filters):
        if filters:
            if isinstance(filters, list):
                self.filter_array.append(f'where {" & ".join(filters)}')
            else:
                self.filter_array.append(f'where {filters.strip()}')
        return self
    
    def construct_options(self, url):
        self.apicalypse = ';'.join(self.filter_array) + ';' if self.filter_array else ''
        options = {
            'url': url or self.config['url']
        }

        if self.config['query_method'] == 'url':
            options['params'] = {
                'apicalypse': self.apicalypse
            }
        elif self.config['query_method'] == 'body':
            # Seems like it should be reversed to prefer query builder
            options['data'] = self.config.get('data') or self.apicalypse
        
        self.config.update(options)
        return self.config
    
    def request(self, url):
        self.construct_options(url)
        config = self.config
        # TODO: Use baseURL
        response = requests.post(config['url'], params=config.get('params'), data=config.get('data'), headers=config.get('headers'))
        # TODO: Use responseType
        return response.json()

def main():
    url = 'https://api-v3.igdb.com/games/'
    igdb = apicalypse({
        'headers': {
            'Accept': 'application/json',
            'user-key': input('Enter your IGDB API key: ')
        },
        # 'responseType': 'json'
    }).fields('*').filter('external_games.uid = "440"')
    print(igdb.construct_options(url))
    print(igdb.request(url))

if __name__ == "__main__":
    main()
