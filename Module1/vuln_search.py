import sys


class Lib:
    def __init__(self, name):
        self.lib_name = name
        self.is_visited = False

        self.dependencies = set()
        self.parents = set()

    def add_lib_dependency(self, dependency):
        self.dependencies = self.dependencies.union(dependency)

    def add_lib_parent(self, parent):
        self.parents.add(parent)


def vuln_search_recursive(path, target, project, proj_libs):
    lib = project[target]
    lib.is_visited = True
    if lib.lib_name in proj_libs:
        print(path)

    for parent in lib.parents:
        if project[parent].is_visited:
            continue
        vuln_search_recursive(parent + ' ' + path, parent, project, proj_libs)

    lib.is_visited = False


# def vuln_search_iterative(start_lib, project, vuln_libs):
#     stack = [(start_lib, [start_lib])]
#     while len(stack):
#         (curr_lib, path) = stack.pop()
#
#         if curr_lib in vuln_libs:
#             print(' '.join(path))
#
#         project[curr_lib].is_visited = True
#
#         for lib_dependency in project[curr_lib].dependencies:
#             stack.append((lib_dependency, path + [lib_dependency]))


def make_proj_graph():
    project = dict()
    vuln_libs = set(input().split())
    proj_libs = set(input().split())

    for lib_name in proj_libs.union(vuln_libs):
        if project.get(lib_name) is None:
            project[lib_name] = Lib(name=lib_name)

    for libs_list in sys.stdin:
        if libs_list == '\n':
            continue

        libs_list = libs_list.rstrip().split()

        for lib_name in libs_list:
            if project.get(lib_name) is None:
                project[lib_name] = Lib(name=lib_name)

        parent = libs_list[0]
        dependencies = libs_list[1:]

        project[parent].add_lib_dependency(dependency=dependencies)

        for dependency in dependencies:
            project[dependency].add_lib_parent(parent=parent)

    return vuln_libs, proj_libs, project


if __name__ == '__main__':

    vulnerable_libs, project_libs, graph = make_proj_graph()

    for vuln_lib in vulnerable_libs:
        vuln_search_recursive(path=vuln_lib, target=vuln_lib, project=graph, proj_libs=project_libs)

    # for proj_lib in project_libs:
    #     vuln_search_iterative(start_lib=proj_lib, project=graph, vuln_libs=vulnerable_libs)