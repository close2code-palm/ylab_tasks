import math
from itertools import combinations, permutations


# Need precisions!

class Point:
    """Represents addressats as points on the
    map(or coordinate plane)"""

    def __init__(self, x: int, y: int, name: str):
        self._name = name
        self.x = x
        self.y = y

    def name(self):
        return self._name


def path_dist_btw2(a: Point, b: Point) -> float:
    """atomic function for calculation distance between neibrough"""
    # from task's picture
    dist_pif = math.sqrt(abs(a.x - b.x) ** 2 + abs(a.y - b.y) ** 2)
    return dist_pif


def path_variants(points: str):
    "Returns all possible paths which can be produced"
    names_pool = ["".join(ad_point) for ad_point in points]

    # we dont take point of departure, so permutations of 4 points
    paths_permuts = permutations(names_pool, r=4)
    full_paths = ["".join(p) for p in paths_permuts]
    full_paths_w_off = map(lambda x: 'p' + x + 'p', full_paths)
    return full_paths_w_off


def main():
    # initialization of map_points
    p = Point(0, 2, 'p')  # post
    a = Point(2, 5, 'a')  # grib
    b = Point(5, 2, 'b')  # beikr_strt
    c = Point(6, 6, 'c')  # bolsh_sad
    d = Point(8, 3, 'd')  # vech_zel

    points_dict = {
        'p': (0, 2),
        'a': (a.x, a.y),
        'b': (b.x, b.y),
        'c': (c.x, c.y),
        'd': (d.x, d.y),
    }

    # FAIL
    # doesnt eval into class object or
    # cant coerce to one from str
    def seg_dist_vals(points: str):
        unit_distances_dict = {}
        path_comb = combinations(points, r=2)
        path_combs_tup = ("".join(cmb) for cmb in path_comb)
        for sgm in path_combs_tup:
            ends = list(sgm)
            # p1 = ends[0]
            # p2 = ends[1]
            p3 = Point(points_dict[ends[0]][0],
                       points_dict[ends[0]][1], ends[0])
            p4 = Point(points_dict[ends[1]][0],
                       points_dict[ends[1]][1],
                       ends[1])
            # p1 = eval(ends[0])
            # p2 = eval(ends[1])
            sgm_extent = path_dist_btw2(p3, p4)
            unit_distances_dict[sgm] = sgm_extent
            unit_distances_dict[sgm[::-1]] = sgm_extent
        return unit_distances_dict

    # building dict with segment extent calculation
    all_paths_dict = seg_dist_vals('pabcd')

    full_extenses_dict = {}

    # building all possible routes, when we start and end
    # our way in post office
    path_pool = path_variants('abcd')

    for way in path_pool:
        dist = 0
        for k in all_paths_dict.keys():
            if k in way:
                dist += all_paths_dict[k]
        full_extenses_dict[way] = dist

    sorted_extenses_dict = sorted(full_extenses_dict,
                                  key=full_extenses_dict.__getitem__)
    best = sorted_extenses_dict[0]  # , sorted_extenses_dict[-1]
    # print(path_pool)
    print(best)
    # print(full_extenses_dict)

    # here we could create an output function,
    # but...no tests here, as in task_repo
    # there was omited 'sadovaya'
    answer_dots = []
    answer_dist = 0
    for dot in (list(best)):
        print(points_dict[dot], end='')
        # break on ! somehow, ref!
        if answer_dots:
            answer_dist += all_paths_dict[answer_dots[-1] + dot]
            print(f'[{answer_dist}]', end='')
        answer_dots.append(dot)
        if answer_dist != full_extenses_dict[best]:
            print(' -> ', end='')
    print(f' = {answer_dist}')


if __name__ == '__main__':
    main()
