import os

import errno
import webbrowser

from controllers.data_base import DataBaseController


class RenderController:

    @classmethod
    def render(cls, category_id):
        print('--------> Quering db for category {}...'.format(category_id))
        try:
            category = DataBaseController().get_category_by_id(category_id)
        except:
            print('--------> No category with ID {}'.format(category_id))
        else:
            print('--------> Building ./html/{}.html file...'.format(category_id))
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
        file.write('        <style>\n')
        file.write('            table {width: 700px; border-collapse: collapse;}\n')
        file.write('            tr:hover {background-color: #eee;}\n')
        file.write('            th {text-align: left;}\n')
        file.write('            td {border: 1px solid #ccc;}\n')
        file.write('        </style>\n')
        file.write('    </head>\n')
        file.write('    <body>\n')
        file.write('        <h1><-------- Engineering Challenge --------></h1>\n')
        file.write('        <p>Click on any category to show/hide children.</p>\n')
        file.write('        <table id="mainTable">\n')
        file.write('            <thead>\n')
        file.write('                <tr>\n')
        file.write('                    <th style="width: 10%">Id</th>\n')
        file.write('                    <th style="width: 70%">Name</th>\n')
        file.write('                    <th style="width: 10%">Level</th>\n')
        file.write('                    <th style="width: 10%">Best Offer</th>\n')
        file.write('                </tr>\n')
        file.write('            </thead>\n')
        file.write('            <tbody>\n')
        file.write('                <tr data-tt-id="{}">\n'.format(category.id))
        file.write('                    <td>{}</td>\n'.format(category.id))
        file.write('                    <td>{}</td>\n'.format(category.name))
        file.write('                    <td>{}</td>\n'.format(category.level))
        file.write('                    <td>{}</td>\n'.format(category.best_offer))
        file.write('                </tr>\n')
        cls._generate_children_rows(category, file)
        file.write('            </tbody>\n')
        file.write('        </table>\n')
        file.write('        <script>\n')
        file.write('            addRowHandlers();\n')
        file.write('            function addRowHandlers() {\n')
        file.write('                var table = document.getElementById("mainTable");\n')
        file.write('                var rows = table.getElementsByTagName("tr");\n')
        file.write('                for (var i = 0; i < rows.length; i++) {\n')
        file.write('                    var currentRow = table.rows[i];\n')
        file.write('                    var createClickHandler = function(row) {\n')
        file.write('                        return function() {\n')
        file.write('                            var children = getChildren(row);\n')
        file.write('                            var firstChild = children[0];\n')
        file.write('                            if (firstChild.style.display !== \'none\') {\n')
        file.write('                                hideChildren(children);\n')
        file.write('                            } else {\n')
        file.write('                                showChildren(children);\n')
        file.write('                            }\n')
        file.write('                        };\n')
        file.write('                    };\n')
        file.write('                    currentRow.onclick = createClickHandler(currentRow);\n')
        file.write('                }\n')
        file.write('            }\n')
        file.write('            function getChildren(row) {\n')
        file.write('                var currentId = row.getAttribute("data-tt-id");\n')
        file.write('                return document.querySelectorAll(\'[data-tt-parent-id="\' + currentId + \'"]\');\n')
        file.write('            }\n')
        file.write('            function hideChildren(children) {\n')
        file.write('                for (var i = 0; i < children.length; i++) {\n')
        file.write('                    var child = children[i];\n')
        file.write('                    child.style.display = \'none\';\n')
        file.write('                    var nestChildren = getChildren(child);\n')
        file.write('                    hideChildren(nestChildren);\n')
        file.write('                }\n')
        file.write('            }\n')
        file.write('            function showChildren(children) {\n')
        file.write('                for (var i = 0; i < children.length; i++) {\n')
        file.write('                    var child = children[i];\n')
        file.write('                    child.style.display = null;\n')
        file.write('                    var nestChildren = getChildren(child);\n')
        file.write('                    showChildren(nestChildren);\n')
        file.write('                }\n')
        file.write('            }\n')
        file.write('        </script>\n')
        file.write('    </body>\n')
        file.write('</html>')
        file.close()
        print('--------> File {} generated!'.format(filename))
        print('--------> File absolute path: {}'.format(os.path.abspath(filename)))

    @classmethod
    def _generate_children_rows(cls, category, file):

        for child in category.children:
            file.write('                <tr data-tt-id="{}" data-tt-parent-id="{}">\n'.format(child.id, child.parent))
            file.write('                    <td>{}</td>\n'.format(child.id))
            file.write('                    <td>{}{}</td>\n'.format('----' * (child.level - 1), child.name))
            file.write('                    <td>{}</td>\n'.format(child.level))
            file.write('                    <td>{}</td>\n'.format(child.best_offer))
            file.write('                </tr>\n')
            cls._generate_children_rows(child, file)
