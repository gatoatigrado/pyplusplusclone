import config

import sys
import web
import form_processor
import code_generator

urls = ( "/", "generator"
        , '/generator.html', 'generator'
        , '/generated.html', 'generated' )

render = web.template.render('templates/')

class generator:
    def GET(self, name=None):
        generator = web.template.frender('templates/generator_tmpl.html')
        return generator()

class generated:
    def POST(self, r_url=None ):
        form = form_processor.generator_t( code_generator.manager_t(), web.input() )
        generated_frender = web.template.frender('templates/generated_tmpl.html')
        generated, warnings = form.process()
        return generated_frender(generated, warnings)

if __name__ == '__main__':
    app = web.application(urls, globals(), autoreload=True)
    app.run()
