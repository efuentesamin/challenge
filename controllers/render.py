import os

import errno

from controllers.data_base import DataBaseController


class RenderController:

    @classmethod
    def render(cls, category_id):
        print('--------> Quering db for category {}...'.format(category_id))
        category = DataBaseController().get_category_by_id(category_id)
        print('--------> Building {}.html file...'.format(category_id))
        cls._generate_html(category)

    @classmethod
    def _generate_html(cls, category):
        """
        Generates the html file
        :param category: 
        :return: 
        """
        filename = "./html/{}.html".format(category.id)

        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise

        file = open(filename, 'w')
        file.write('<html>\n')
        file.write('    <head>\n')
        file.write('        <title>Category {}</title>\n'.format(category.id))
        file.write('    </head>\n')
        file.write('    <body>\n')
        file.write('        <table summary="folder contents for fly types">\n')
        file.write('            <thead>\n')
        file.write('                <tr>\n')
        file.write('                    <th class="name">Name</th>\n')
        file.write('                    <th class="location">Location</th>\n')
        file.write('                    <th class="color">Color</th>\n')
        file.write('                </tr>\n')
        file.write('            </thead>\n')
        file.write('            <tbody>\n')
        file.write('                <tr>\n')
        file.write('                    <th colspan="3">House</th>\n')
        file.write('                </tr>\n')
        file.write('                <tr>\n')
        file.write('                    <th class="start">Carrion Fly</th>\n')
        file.write('                    <td>Worldwide</td>\n')
        file.write('                    <td>gray</td>\n')
        file.write('                </tr>\n')
        file.write('                <tr>\n')
        file.write('                    <th class="start">Office Fly</th>\n')
        file.write('                    <td>California, Bay Area</td>\n')
        file.write('                    <td>white</td>\n')
        file.write('                </tr>\n')
        file.write('                <tr>\n')
        file.write('                    <th class="end">Common House Fly</th>\n')
        file.write('                    <td></td>\n')
        file.write('                    <td>brown</td>\n')
        file.write('                </tr>\n')
        file.write('                <tr>\n')
        file.write('                    <th colspan="3">Horse</th>\n')
        file.write('                </tr>\n')
        file.write('                <tr>\n')
        file.write('                    <th class="start">Horn Fly</th>\n')
        file.write('                    <td>Kansas</td>\n')
        file.write('                    <td>red</td>\n')
        file.write('                </tr>\n')
        file.write('                <tr>\n')
        file.write('                    <th class="start">Face Fly</th>\n')
        file.write('                    <td></td>\n')
        file.write('                    <td>green</td>\n')
        file.write('                </tr>\n')
        file.write('                <tr class="end">\n')
        file.write('                    <th class="end">Stable Fly</th>\n')
        file.write('                    <td></td>\n')
        file.write('                    <td>black</td>\n')
        file.write('                </tr>\n')
        file.write('            </tbody>\n')
        file.write('        </table>\n')
        file.write('    </body>\n')
        file.write('</html>')
        file.close()
        print('--------> File {}.html generated!'.format(category.id))
