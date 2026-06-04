from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw

from run_fretboard_answer_bbox_tasks import ROOT, rel_path, workspace_path


OUTPUT_ROOT = ROOT / "data" / "processed" / "fretboard_handbook" / "bbox_tasks"


MANUAL_LAYOUTS: dict[str, dict[str, Any]] = {
    "exercise_01_05": {
        "image_path": "data/练习解答（图片）/练习1-练习5.png",
        "items": [
            {
                "exercise": 3,
                "subquestion": "all",
                "bbox": [34, 303, 138, 562],
                "evidence_type": "text_answer_ocr",
                "notes": "pure text answer block for VLM OCR",
            },
            {"exercise": 4, "subquestion": 1, "bbox": [482, 306, 563, 431]},
            {"exercise": 4, "subquestion": 2, "bbox": [580, 308, 661, 431]},
            {"exercise": 4, "subquestion": 3, "bbox": [676, 307, 757, 431]},
            {"exercise": 4, "subquestion": 4, "bbox": [774, 307, 855, 431]},
            {"exercise": 4, "subquestion": 5, "bbox": [870, 307, 951, 431]},
            {"exercise": 4, "subquestion": 6, "bbox": [482, 432, 563, 559]},
            {"exercise": 4, "subquestion": 7, "bbox": [580, 432, 661, 559]},
            {"exercise": 4, "subquestion": 8, "bbox": [676, 432, 757, 559]},
            {"exercise": 4, "subquestion": 9, "bbox": [774, 432, 855, 559]},
            {"exercise": 4, "subquestion": 10, "bbox": [870, 432, 951, 559]},
            {"exercise": 5, "subquestion": 1, "bbox": [34, 624, 474, 691]},
            {"exercise": 5, "subquestion": 2, "bbox": [34, 716, 474, 784]},
            {"exercise": 5, "subquestion": 3, "bbox": [34, 807, 474, 876]},
            {"exercise": 5, "subquestion": 4, "bbox": [34, 898, 474, 967]},
            {"exercise": 5, "subquestion": 5, "bbox": [34, 989, 474, 1057]},
            {"exercise": 5, "subquestion": 6, "bbox": [491, 624, 932, 691]},
            {"exercise": 5, "subquestion": 7, "bbox": [491, 716, 932, 784]},
            {"exercise": 5, "subquestion": 8, "bbox": [491, 807, 932, 876]},
            {"exercise": 5, "subquestion": 9, "bbox": [491, 898, 932, 967]},
            {"exercise": 5, "subquestion": 10, "bbox": [491, 989, 932, 1057]},
        ],
    },
    "exercise_06_09": {
        "image_path": "data/练习解答（图片）/练习6-练习9.png",
        "items": [
            {"exercise": 6, "subquestion": 1, "bbox": [15, 76, 421, 155]},
            {"exercise": 6, "subquestion": 2, "bbox": [15, 155, 421, 231]},
            {"exercise": 6, "subquestion": 3, "bbox": [15, 232, 421, 308]},
            {"exercise": 6, "subquestion": 4, "bbox": [14, 309, 421, 384]},
            {"exercise": 6, "subquestion": 5, "bbox": [14, 385, 421, 460]},
            {"exercise": 6, "subquestion": 6, "bbox": [14, 459, 421, 535]},
            {"exercise": 7, "subquestion": 1, "bbox": [468, 76, 876, 164]},
            {"exercise": 7, "subquestion": 2, "bbox": [468, 155, 876, 241]},
            {"exercise": 7, "subquestion": 3, "bbox": [468, 232, 876, 318]},
            {"exercise": 7, "subquestion": 4, "bbox": [468, 309, 876, 393]},
            {"exercise": 7, "subquestion": 5, "bbox": [468, 386, 876, 470]},
            {"exercise": 7, "subquestion": 6, "bbox": [468, 463, 876, 546]},
            {"exercise": 8, "subquestion": 1, "bbox": [16, 706, 421, 787]},
            {"exercise": 8, "subquestion": 2, "bbox": [16, 786, 421, 864]},
            {"exercise": 8, "subquestion": 3, "bbox": [15, 864, 421, 941]},
            {"exercise": 8, "subquestion": 4, "bbox": [15, 940, 421, 1017]},
            {"exercise": 8, "subquestion": 5, "bbox": [15, 1015, 421, 1094]},
            {"exercise": 8, "subquestion": 6, "bbox": [15, 1090, 421, 1168]},
            {
                "exercise": 9,
                "subquestion": "all",
                "bbox": [465, 625, 610, 1106],
                "evidence_type": "text_answer_ocr",
                "notes": "pure text answer block for VLM OCR",
            },
        ],
    },
    "exercise_10_11": {
        "image_path": "data/练习解答（图片）/练习10-练习11.png",
        "items": [
            {"exercise": 10, "subquestion": 1, "bbox": [42, 116, 612, 212]},
            {"exercise": 10, "subquestion": 2, "bbox": [42, 224, 612, 324]},
            {"exercise": 10, "subquestion": 3, "bbox": [42, 340, 612, 436]},
            {"exercise": 10, "subquestion": 4, "bbox": [42, 452, 612, 548]},
            {"exercise": 10, "subquestion": 5, "bbox": [42, 560, 612, 660]},
            {"exercise": 10, "subquestion": 6, "bbox": [42, 672, 612, 772]},
            {"exercise": 10, "subquestion": 7, "bbox": [42, 792, 612, 906]},
            {"exercise": 10, "subquestion": 8, "bbox": [42, 906, 612, 1004]},
            {"exercise": 10, "subquestion": 9, "bbox": [42, 1018, 614, 1118]},
            {"exercise": 10, "subquestion": 10, "bbox": [40, 1130, 614, 1230]},
            {"exercise": 11, "subquestion": 1, "bbox": [722, 114, 1410, 208]},
            {"exercise": 11, "subquestion": 2, "bbox": [728, 244, 1410, 330]},
            {"exercise": 11, "subquestion": 3, "bbox": [728, 362, 1410, 448]},
            {"exercise": 11, "subquestion": 4, "bbox": [728, 474, 1410, 560]},
            {"exercise": 11, "subquestion": 5, "bbox": [728, 584, 1410, 672]},
            {"exercise": 11, "subquestion": 6, "bbox": [730, 684, 1412, 770]},
            {"exercise": 11, "subquestion": 7, "bbox": [730, 794, 1412, 882]},
            {"exercise": 11, "subquestion": 8, "bbox": [730, 908, 1412, 994]},
            {"exercise": 11, "subquestion": 9, "bbox": [730, 1022, 1412, 1118]},
            {"exercise": 11, "subquestion": 10, "bbox": [730, 1138, 1412, 1226]},
        ],
    },
    "exercise_12_12": {
        "image_path": "data/练习解答（图片）/练习12.png",
        "items": [
            {"exercise": 12, "subquestion": 1, "bbox": [64, 58, 632, 166]},
            {"exercise": 12, "subquestion": 2, "bbox": [64, 198, 632, 303]},
            {"exercise": 12, "subquestion": 3, "bbox": [64, 335, 632, 440]},
            {"exercise": 12, "subquestion": 4, "bbox": [65, 472, 632, 576]},
            {"exercise": 12, "subquestion": 5, "bbox": [65, 609, 633, 715]},
            {"exercise": 12, "subquestion": 6, "bbox": [700, 72, 1270, 177]},
            {"exercise": 12, "subquestion": 7, "bbox": [701, 211, 1270, 318]},
            {"exercise": 12, "subquestion": 8, "bbox": [700, 348, 1270, 453]},
            {"exercise": 12, "subquestion": 9, "bbox": [698, 486, 1271, 591]},
            {"exercise": 12, "subquestion": 10, "bbox": [698, 623, 1271, 728]},
        ],
    },
    "exercise_13_14": {
        "image_path": "data/练习解答（图片）/练习13-练习14.png",
        "items": [
            {"exercise": 13, "subquestion": 1, "bbox": [45, 78, 665, 202]},
            {"exercise": 13, "subquestion": 2, "bbox": [43, 208, 665, 328]},
            {"exercise": 13, "subquestion": 3, "bbox": [43, 328, 665, 447]},
            {"exercise": 13, "subquestion": 4, "bbox": [44, 451, 664, 570]},
            {"exercise": 13, "subquestion": 5, "bbox": [43, 575, 664, 704]},
            {"exercise": 13, "subquestion": 6, "bbox": [48, 698, 670, 821]},
            {"exercise": 13, "subquestion": 7, "bbox": [47, 823, 670, 942]},
            {"exercise": 13, "subquestion": 8, "bbox": [47, 942, 670, 1065]},
            {"exercise": 13, "subquestion": 9, "bbox": [47, 1063, 670, 1190]},
            {"exercise": 13, "subquestion": 10, "bbox": [47, 1186, 670, 1308]},
            {"exercise": 14, "subquestion": 1, "bbox": [798, 78, 1420, 205]},
            {"exercise": 14, "subquestion": 2, "bbox": [796, 209, 1420, 327]},
            {"exercise": 14, "subquestion": 3, "bbox": [796, 328, 1420, 447]},
            {"exercise": 14, "subquestion": 4, "bbox": [797, 451, 1419, 570]},
            {"exercise": 14, "subquestion": 5, "bbox": [796, 578, 1419, 697]},
            {"exercise": 14, "subquestion": 6, "bbox": [801, 700, 1425, 822]},
            {"exercise": 14, "subquestion": 7, "bbox": [801, 822, 1425, 941]},
            {"exercise": 14, "subquestion": 8, "bbox": [800, 944, 1425, 1064]},
            {"exercise": 14, "subquestion": 9, "bbox": [801, 1066, 1425, 1190]},
            {"exercise": 14, "subquestion": 10, "bbox": [801, 1186, 1425, 1310]},
        ],
    },
    "exercise_15_15": {
        "image_path": "data/练习解答（图片）/练习15.png",
        "items": [
            {"exercise": 15, "subquestion": 1, "bbox": [22, 88, 636, 214]},
            {"exercise": 15, "subquestion": 2, "bbox": [16, 242, 636, 366]},
            {"exercise": 15, "subquestion": 3, "bbox": [16, 394, 636, 518]},
            {"exercise": 15, "subquestion": 4, "bbox": [16, 546, 636, 668]},
            {"exercise": 15, "subquestion": 5, "bbox": [15, 696, 636, 821]},
            {"exercise": 15, "subquestion": 6, "bbox": [736, 90, 1358, 214]},
            {"exercise": 15, "subquestion": 7, "bbox": [736, 240, 1358, 367]},
            {"exercise": 15, "subquestion": 8, "bbox": [736, 394, 1358, 516]},
            {"exercise": 15, "subquestion": 9, "bbox": [730, 546, 1358, 670]},
            {"exercise": 15, "subquestion": 10, "bbox": [730, 696, 1358, 818]},
        ],
    },
    "exercise_16_19": {
        "image_path": "data/练习解答（图片）/练习16-练习19.png",
        "items": [
            {"exercise": 16, "subquestion": 1, "bbox": [22, 116, 142, 362]},
            {"exercise": 16, "subquestion": 2, "bbox": [174, 116, 302, 362]},
            {"exercise": 16, "subquestion": 3, "bbox": [325, 136, 450, 362]},
            {"exercise": 16, "subquestion": 4, "bbox": [482, 137, 603, 363]},
            {"exercise": 16, "subquestion": 5, "bbox": [629, 118, 754, 365]},
            {"exercise": 17, "subquestion": 1, "bbox": [777, 118, 891, 365]},
            {"exercise": 17, "subquestion": 2, "bbox": [927, 118, 1057, 365]},
            {"exercise": 17, "subquestion": 3, "bbox": [1075, 120, 1206, 366]},
            {"exercise": 17, "subquestion": 4, "bbox": [1228, 120, 1358, 366]},
            {"exercise": 17, "subquestion": 5, "bbox": [1382, 120, 1499, 366]},
            {"exercise": 18, "subquestion": 1, "bbox": [25, 477, 151, 739]},
            {"exercise": 18, "subquestion": 2, "bbox": [181, 477, 304, 739]},
            {"exercise": 18, "subquestion": 3, "bbox": [333, 487, 454, 739]},
            {"exercise": 18, "subquestion": 4, "bbox": [472, 498, 608, 740]},
            {"exercise": 18, "subquestion": 5, "bbox": [636, 478, 757, 740]},
            {"exercise": 19, "subquestion": 1, "bbox": [782, 478, 903, 740]},
            {"exercise": 19, "subquestion": 2, "bbox": [937, 478, 1062, 740]},
            {"exercise": 19, "subquestion": 3, "bbox": [1082, 478, 1209, 739]},
            {"exercise": 19, "subquestion": 4, "bbox": [1232, 478, 1363, 739]},
            {"exercise": 19, "subquestion": 5, "bbox": [1388, 478, 1510, 739]},
        ],
    },
    "exercise_20_21": {
        "image_path": "data/练习解答（图片）/练习20-练习21.png",
        "items": [
            {"exercise": 20, "subquestion": 1, "bbox": [82, 80, 205, 323]},
            {"exercise": 20, "subquestion": 2, "bbox": [232, 80, 358, 323]},
            {"exercise": 20, "subquestion": 3, "bbox": [387, 99, 510, 323]},
            {"exercise": 20, "subquestion": 4, "bbox": [539, 100, 663, 323]},
            {"exercise": 20, "subquestion": 5, "bbox": [689, 80, 815, 323]},
            {"exercise": 20, "subquestion": 6, "bbox": [838, 80, 963, 323]},
            {"exercise": 20, "subquestion": 7, "bbox": [994, 98, 1116, 321]},
            {"exercise": 20, "subquestion": 8, "bbox": [1142, 78, 1268, 322]},
            {"exercise": 20, "subquestion": 9, "bbox": [1291, 78, 1410, 322]},
            {"exercise": 20, "subquestion": 10, "bbox": [1443, 78, 1563, 322]},
            {"exercise": 21, "subquestion": 1, "bbox": [80, 444, 196, 687]},
            {"exercise": 21, "subquestion": 2, "bbox": [230, 444, 350, 687]},
            {"exercise": 21, "subquestion": 3, "bbox": [384, 464, 507, 687]},
            {"exercise": 21, "subquestion": 4, "bbox": [533, 464, 659, 687]},
            {"exercise": 21, "subquestion": 5, "bbox": [682, 445, 810, 688]},
            {"exercise": 21, "subquestion": 6, "bbox": [827, 445, 967, 688]},
            {"exercise": 21, "subquestion": 7, "bbox": [988, 460, 1117, 685]},
            {"exercise": 21, "subquestion": 8, "bbox": [1135, 444, 1273, 686]},
            {"exercise": 21, "subquestion": 9, "bbox": [1283, 444, 1426, 686]},
            {"exercise": 21, "subquestion": 10, "bbox": [1428, 444, 1572, 686]},
        ],
    },
    "exercise_22_22": {
        "image_path": "data/练习解答（图片）/练习22.png",
        "items": [
            {"exercise": 22, "subquestion": 1, "bbox": [33, 76, 156, 360], "part": 1},
            {"exercise": 22, "subquestion": 2, "bbox": [182, 76, 312, 360], "part": 1},
            {"exercise": 22, "subquestion": 3, "bbox": [336, 96, 464, 361], "part": 1},
            {"exercise": 22, "subquestion": 4, "bbox": [489, 96, 609, 361], "part": 1},
            {"exercise": 22, "subquestion": 5, "bbox": [639, 96, 762, 361], "part": 1},
            {"exercise": 22, "subquestion": 6, "bbox": [787, 96, 907, 360], "part": 1},
            {"exercise": 22, "subquestion": 7, "bbox": [939, 96, 1059, 360], "part": 1},
            {"exercise": 22, "subquestion": 8, "bbox": [1090, 96, 1211, 360], "part": 1},
            {"exercise": 22, "subquestion": 9, "bbox": [1241, 96, 1364, 361], "part": 1},
            {"exercise": 22, "subquestion": 10, "bbox": [1391, 77, 1512, 361], "part": 1},
            {"exercise": 22, "subquestion": 1, "bbox": [30, 394, 148, 678], "part": 2},
            {"exercise": 22, "subquestion": 2, "bbox": [180, 394, 306, 678], "part": 2},
            {"exercise": 22, "subquestion": 3, "bbox": [332, 403, 457, 678], "part": 2},
            {"exercise": 22, "subquestion": 4, "bbox": [480, 414, 608, 678], "part": 2},
            {"exercise": 22, "subquestion": 5, "bbox": [633, 404, 757, 679], "part": 2},
            {"exercise": 22, "subquestion": 6, "bbox": [788, 405, 910, 683], "part": 2},
            {"exercise": 22, "subquestion": 7, "bbox": [937, 417, 1062, 683], "part": 2},
            {"exercise": 22, "subquestion": 8, "bbox": [1092, 419, 1216, 683], "part": 2},
            {"exercise": 22, "subquestion": 9, "bbox": [1239, 419, 1370, 683], "part": 2},
            {"exercise": 22, "subquestion": 10, "bbox": [1389, 400, 1521, 684], "part": 2},
        ],
    },
    "exercise_23_23": {
        "image_path": "data/练习解答（图片）/练习23.png",
        "items": [
            {
                "exercise": 23,
                "subquestion": "all",
                "bbox": [25, 100, 1338, 1148],
                "evidence_type": "text_answer_ocr",
                "notes": "pure text answer page for VLM OCR",
            },
        ],
    },
    "exercise_24_26": {
        "image_path": "data/练习解答（图片）/练习24-26.png",
        "items": [
            {"exercise": 24, "subquestion": 1, "bbox": [17, 80, 115, 272]},
            {"exercise": 24, "subquestion": 2, "bbox": [160, 80, 256, 272]},
            {"exercise": 24, "subquestion": 3, "bbox": [302, 80, 398, 272]},
            {"exercise": 24, "subquestion": 4, "bbox": [443, 80, 541, 272]},
            {"exercise": 24, "subquestion": 5, "bbox": [586, 80, 686, 272]},
            {"exercise": 24, "subquestion": 6, "bbox": [723, 79, 821, 271]},
            {"exercise": 24, "subquestion": 7, "bbox": [867, 79, 963, 271]},
            {"exercise": 24, "subquestion": 8, "bbox": [1004, 79, 1106, 271]},
            {"exercise": 24, "subquestion": 9, "bbox": [1154, 79, 1247, 271]},
            {"exercise": 24, "subquestion": 10, "bbox": [1287, 79, 1389, 271]},
            {"exercise": 25, "subquestion": 1, "bbox": [17, 357, 115, 561]},
            {"exercise": 25, "subquestion": 2, "bbox": [160, 357, 256, 561]},
            {"exercise": 25, "subquestion": 3, "bbox": [302, 357, 398, 561]},
            {"exercise": 25, "subquestion": 4, "bbox": [436, 357, 540, 561]},
            {"exercise": 25, "subquestion": 5, "bbox": [587, 357, 682, 561]},
            {"exercise": 25, "subquestion": 6, "bbox": [723, 357, 820, 560]},
            {"exercise": 25, "subquestion": 7, "bbox": [869, 357, 963, 560]},
            {"exercise": 25, "subquestion": 8, "bbox": [998, 357, 1105, 560]},
            {"exercise": 25, "subquestion": 9, "bbox": [1151, 357, 1247, 560]},
            {"exercise": 25, "subquestion": 10, "bbox": [1276, 357, 1389, 560]},
            {"exercise": 26, "subquestion": 1, "bbox": [22, 660, 113, 854]},
            {"exercise": 26, "subquestion": 2, "bbox": [119, 660, 211, 854]},
            {"exercise": 26, "subquestion": 3, "bbox": [220, 660, 312, 854]},
            {"exercise": 26, "subquestion": 4, "bbox": [319, 660, 410, 854]},
            {"exercise": 26, "subquestion": 5, "bbox": [420, 660, 509, 854]},
            {"exercise": 26, "subquestion": 6, "bbox": [518, 660, 610, 854]},
            {"exercise": 26, "subquestion": 7, "bbox": [617, 660, 709, 854]},
            {"exercise": 26, "subquestion": 8, "bbox": [721, 660, 812, 854]},
            {"exercise": 26, "subquestion": 9, "bbox": [813, 660, 902, 854]},
            {"exercise": 26, "subquestion": 10, "bbox": [903, 660, 995, 854]},
            {"exercise": 26, "subquestion": 11, "bbox": [995, 660, 1088, 854]},
            {"exercise": 26, "subquestion": 12, "bbox": [1088, 660, 1180, 854]},
            {"exercise": 26, "subquestion": 13, "bbox": [1180, 660, 1272, 854]},
            {"exercise": 26, "subquestion": 14, "bbox": [1273, 660, 1363, 854]},
            {"exercise": 26, "subquestion": 15, "bbox": [1363, 660, 1454, 854]},
        ],
    },
    "exercise_28_29": {
        "image_path": "data/练习解答（图片）/练习28-29.png",
        "items": [
            {"exercise": 28, "subquestion": 1, "bbox": [29, 114, 121, 288]},
            {"exercise": 28, "subquestion": 2, "bbox": [166, 114, 263, 288]},
            {"exercise": 28, "subquestion": 3, "bbox": [314, 114, 405, 287]},
            {"exercise": 28, "subquestion": 4, "bbox": [451, 114, 547, 287]},
            {"exercise": 28, "subquestion": 5, "bbox": [598, 90, 690, 287]},
            {"exercise": 28, "subquestion": 6, "bbox": [738, 90, 829, 287]},
            {"exercise": 28, "subquestion": 7, "bbox": [875, 90, 971, 287]},
            {"exercise": 28, "subquestion": 8, "bbox": [1021, 113, 1114, 287]},
            {"exercise": 28, "subquestion": 9, "bbox": [1164, 113, 1256, 287]},
            {"exercise": 28, "subquestion": 10, "bbox": [1305, 114, 1397, 287]},
            {
                "exercise": 29,
                "subquestion": "all",
                "bbox": [30, 365, 985, 535],
                "evidence_type": "text_answer_ocr",
                "notes": "pure text answer block for VLM OCR",
            },
        ],
    },
    "exercise_30_33": {
        "image_path": "data/练习解答（图片）/练习30-33.png",
        "items": [
            {"exercise": 30, "subquestion": 1, "bbox": [37, 85, 238, 212]},
            {"exercise": 30, "subquestion": 2, "bbox": [36, 224, 238, 347]},
            {"exercise": 30, "subquestion": 3, "bbox": [39, 362, 238, 500]},
            {"exercise": 30, "subquestion": 4, "bbox": [37, 501, 237, 625]},
            {"exercise": 30, "subquestion": 5, "bbox": [35, 639, 237, 764]},
            {"exercise": 31, "subquestion": 1, "bbox": [434, 85, 635, 209]},
            {"exercise": 31, "subquestion": 2, "bbox": [432, 223, 635, 347]},
            {"exercise": 31, "subquestion": 3, "bbox": [435, 362, 635, 501]},
            {"exercise": 31, "subquestion": 4, "bbox": [435, 501, 634, 629]},
            {"exercise": 31, "subquestion": 5, "bbox": [432, 640, 634, 782]},
            {"exercise": 32, "subquestion": 1, "bbox": [827, 85, 1028, 209]},
            {"exercise": 32, "subquestion": 2, "bbox": [826, 223, 1028, 347]},
            {"exercise": 32, "subquestion": 3, "bbox": [825, 362, 1027, 496]},
            {"exercise": 32, "subquestion": 4, "bbox": [828, 501, 1027, 628]},
            {"exercise": 32, "subquestion": 5, "bbox": [825, 640, 1027, 764]},
            {"exercise": 33, "subquestion": 1, "bbox": [1221, 84, 1420, 211]},
            {"exercise": 33, "subquestion": 2, "bbox": [1218, 222, 1421, 347]},
            {"exercise": 33, "subquestion": 3, "bbox": [1218, 362, 1420, 495]},
            {"exercise": 33, "subquestion": 4, "bbox": [1220, 501, 1420, 630]},
            {"exercise": 33, "subquestion": 5, "bbox": [1218, 640, 1420, 766]},
        ],
    },
    "exercise_34_37": {
        "image_path": "data/练习解答（图片）/练习34-37.png",
        "items": [
            {"exercise": 34, "subquestion": 1, "bbox": [56, 84, 188, 304]},
            {"exercise": 34, "subquestion": 2, "bbox": [194, 84, 344, 304]},
            {"exercise": 34, "subquestion": 3, "bbox": [348, 84, 486, 304]},
            {"exercise": 35, "subquestion": 1, "bbox": [757, 83, 895, 304]},
            {"exercise": 35, "subquestion": 2, "bbox": [906, 83, 1044, 304]},
            {"exercise": 35, "subquestion": 3, "bbox": [1058, 83, 1197, 304]},
            {"exercise": 36, "subquestion": 1, "bbox": [50, 462, 181, 638]},
            {"exercise": 36, "subquestion": 2, "bbox": [196, 462, 331, 638]},
            {"exercise": 36, "subquestion": 3, "bbox": [342, 462, 481, 638]},
            {"exercise": 37, "subquestion": 1, "bbox": [751, 462, 890, 638]},
            {"exercise": 37, "subquestion": 2, "bbox": [904, 462, 1047, 638]},
            {"exercise": 37, "subquestion": 3, "bbox": [1050, 462, 1188, 638]},
        ],
    },
    "exercise_39_42": {
        "image_path": "data/练习解答（图片）/练习39-42.png",
        "items": [
            {"exercise": 38, "subquestion": 1, "bbox": [52, 117, 297, 271]},
            {"exercise": 38, "subquestion": 2, "bbox": [51, 290, 297, 444]},
            {"exercise": 38, "subquestion": 3, "bbox": [54, 463, 297, 635]},
            {"exercise": 38, "subquestion": 4, "bbox": [54, 636, 297, 806]},
            {"exercise": 38, "subquestion": 5, "bbox": [51, 809, 297, 983]},
            {"exercise": 39, "subquestion": 1, "bbox": [437, 116, 682, 274]},
            {"exercise": 39, "subquestion": 2, "bbox": [435, 289, 682, 442]},
            {"exercise": 39, "subquestion": 3, "bbox": [434, 462, 682, 615]},
            {"exercise": 39, "subquestion": 4, "bbox": [438, 635, 682, 808]},
            {"exercise": 39, "subquestion": 5, "bbox": [435, 808, 682, 966]},
            {"exercise": 40, "subquestion": 1, "bbox": [826, 116, 1072, 269]},
            {"exercise": 40, "subquestion": 2, "bbox": [824, 288, 1072, 443]},
            {"exercise": 40, "subquestion": 3, "bbox": [828, 461, 1072, 632]},
            {"exercise": 40, "subquestion": 4, "bbox": [826, 634, 1072, 791]},
            {"exercise": 40, "subquestion": 5, "bbox": [825, 807, 1072, 981]},
            {"exercise": 41, "subquestion": 1, "bbox": [1218, 116, 1465, 274]},
            {"exercise": 41, "subquestion": 2, "bbox": [1217, 289, 1465, 442]},
            {"exercise": 41, "subquestion": 3, "bbox": [1217, 462, 1465, 627]},
            {"exercise": 41, "subquestion": 4, "bbox": [1220, 635, 1465, 807]},
            {"exercise": 41, "subquestion": 5, "bbox": [1217, 808, 1465, 966]},
            {"exercise": 42, "subquestion": 1, "bbox": [1612, 114, 1858, 268]},
            {"exercise": 42, "subquestion": 2, "bbox": [1610, 287, 1858, 439]},
            {"exercise": 42, "subquestion": 3, "bbox": [1613, 459, 1858, 632]},
            {"exercise": 42, "subquestion": 4, "bbox": [1612, 632, 1858, 790]},
            {"exercise": 42, "subquestion": 5, "bbox": [1610, 805, 1858, 979]},
        ],
    },
    "exercise_43_46": {
        "image_path": "data/练习解答（图片）/练习43-46.png",
        "items": [
            {"exercise": 43, "subquestion": 1, "bbox": [43, 83, 155, 310]},
            {"exercise": 43, "subquestion": 2, "bbox": [202, 83, 321, 310]},
            {"exercise": 43, "subquestion": 3, "bbox": [369, 83, 487, 309]},
            {"exercise": 43, "subquestion": 4, "bbox": [538, 82, 654, 309]},
            {"exercise": 43, "subquestion": 5, "bbox": [704, 82, 821, 309]},
            {"exercise": 44, "subquestion": 1, "bbox": [35, 514, 149, 741]},
            {"exercise": 44, "subquestion": 2, "bbox": [197, 514, 316, 741]},
            {"exercise": 44, "subquestion": 3, "bbox": [366, 514, 481, 740]},
            {"exercise": 44, "subquestion": 4, "bbox": [535, 513, 648, 740]},
            {"exercise": 44, "subquestion": 5, "bbox": [701, 513, 815, 739]},
            {"exercise": 44, "subquestion": 6, "bbox": [867, 512, 984, 739]},
            {"exercise": 44, "subquestion": 7, "bbox": [1029, 512, 1151, 739]},
            {"exercise": 44, "subquestion": 8, "bbox": [1195, 511, 1318, 738]},
            {"exercise": 44, "subquestion": 9, "bbox": [1363, 511, 1486, 737]},
            {"exercise": 44, "subquestion": 10, "bbox": [1529, 510, 1653, 737]},
            {"exercise": 45, "subquestion": 1, "bbox": [38, 946, 154, 1173]},
            {"exercise": 45, "subquestion": 2, "bbox": [199, 946, 320, 1173]},
            {"exercise": 45, "subquestion": 3, "bbox": [371, 946, 487, 1172]},
            {"exercise": 45, "subquestion": 4, "bbox": [538, 946, 654, 1172]},
            {"exercise": 45, "subquestion": 5, "bbox": [704, 945, 821, 1172]},
            {"exercise": 46, "subquestion": 1, "bbox": [863, 945, 980, 1171]},
            {"exercise": 46, "subquestion": 2, "bbox": [1025, 945, 1147, 1171]},
            {"exercise": 46, "subquestion": 3, "bbox": [1197, 944, 1312, 1171]},
            {"exercise": 46, "subquestion": 4, "bbox": [1364, 944, 1482, 1170]},
            {"exercise": 46, "subquestion": 5, "bbox": [1531, 944, 1649, 1170]},
        ],
    },
    "exercise_47_48": {
        "image_path": "data/练习解答（图片）/练习47-48.png",
        "items": [
            {"exercise": 47, "subquestion": 1, "bbox": [28, 112, 156, 366]},
            {"exercise": 47, "subquestion": 2, "bbox": [199, 112, 332, 366]},
            {"exercise": 47, "subquestion": 3, "bbox": [380, 112, 508, 366]},
            {"exercise": 48, "subquestion": 1, "bbox": [866, 112, 1106, 270]},
            {"exercise": 48, "subquestion": 2, "bbox": [1192, 144, 1438, 286]},
            {"exercise": 48, "subquestion": 3, "bbox": [1464, 128, 1706, 288]},
            {"exercise": 48, "subquestion": 4, "bbox": [864, 286, 1106, 450]},
            {"exercise": 48, "subquestion": 5, "bbox": [1194, 292, 1438, 448]},
            {"exercise": 48, "subquestion": 6, "bbox": [1464, 292, 1706, 462]},
            {"exercise": 48, "subquestion": 7, "bbox": [878, 456, 1106, 596]},
            {"exercise": 48, "subquestion": 8, "bbox": [1192, 462, 1438, 616]},
            {"exercise": 48, "subquestion": 9, "bbox": [1462, 460, 1706, 616]},
            {"exercise": 48, "subquestion": 10, "bbox": [878, 616, 1106, 762]},
            {"exercise": 48, "subquestion": 11, "bbox": [1192, 624, 1438, 792]},
            {"exercise": 48, "subquestion": 12, "bbox": [1462, 620, 1706, 778]},
            {"exercise": 48, "subquestion": 13, "bbox": [878, 780, 1106, 938]},
            {"exercise": 48, "subquestion": 14, "bbox": [1192, 784, 1438, 946]},
            {"exercise": 48, "subquestion": 15, "bbox": [1462, 784, 1706, 946]},
        ],
    },
    "exercise_49_51": {
        "image_path": "data/练习解答（图片）/练习49-51.png",
        "items": [
            {"exercise": 49, "subquestion": 1, "bbox": [24, 88, 150, 323]},
            {"exercise": 49, "subquestion": 2, "bbox": [186, 88, 315, 323]},
            {"exercise": 49, "subquestion": 3, "bbox": [350, 88, 482, 323]},
            {"exercise": 49, "subquestion": 4, "bbox": [520, 88, 650, 323]},
            {"exercise": 49, "subquestion": 5, "bbox": [690, 88, 818, 323]},
            {"exercise": 49, "subquestion": 6, "bbox": [856, 88, 988, 323]},
            {"exercise": 49, "subquestion": 7, "bbox": [1022, 88, 1155, 323]},
            {"exercise": 49, "subquestion": 8, "bbox": [1185, 88, 1320, 323]},
            {"exercise": 49, "subquestion": 9, "bbox": [1355, 88, 1490, 323]},
            {"exercise": 49, "subquestion": 10, "bbox": [1514, 88, 1650, 323]},
            {"exercise": 50, "subquestion": 1, "bbox": [24, 505, 152, 776]},
            {"exercise": 50, "subquestion": 2, "bbox": [186, 505, 318, 776]},
            {"exercise": 50, "subquestion": 3, "bbox": [354, 505, 488, 776]},
            {"exercise": 50, "subquestion": 4, "bbox": [526, 505, 663, 776]},
            {"exercise": 50, "subquestion": 5, "bbox": [690, 505, 858, 778]},
            {"exercise": 50, "subquestion": 6, "bbox": [866, 505, 995, 778]},
            {"exercise": 50, "subquestion": 7, "bbox": [1026, 505, 1173, 778]},
            {"exercise": 50, "subquestion": 8, "bbox": [1197, 505, 1328, 778]},
            {"exercise": 50, "subquestion": 9, "bbox": [1366, 505, 1495, 778]},
            {"exercise": 50, "subquestion": 10, "bbox": [1530, 505, 1685, 778]},
            {"exercise": 51, "subquestion": 1, "bbox": [22, 962, 156, 1204]},
            {"exercise": 51, "subquestion": 2, "bbox": [194, 962, 320, 1204]},
            {"exercise": 51, "subquestion": 3, "bbox": [358, 962, 492, 1204]},
            {"exercise": 51, "subquestion": 4, "bbox": [526, 962, 653, 1204]},
            {"exercise": 51, "subquestion": 5, "bbox": [688, 962, 824, 1204]},
            {"exercise": 51, "subquestion": 6, "bbox": [854, 962, 982, 1204]},
            {"exercise": 51, "subquestion": 7, "bbox": [1026, 962, 1150, 1204]},
            {"exercise": 51, "subquestion": 8, "bbox": [1183, 962, 1314, 1204]},
            {"exercise": 51, "subquestion": 9, "bbox": [1356, 962, 1482, 1204]},
            {"exercise": 51, "subquestion": 10, "bbox": [1514, 962, 1648, 1204]},
        ],
    },
    "exercise_52_52": {
        "image_path": "data/练习解答（图片）/练习52.png",
        "items": [
            {
                "exercise": 52,
                "subquestion": "all",
                "bbox": [0, 0, 480, 444],
                "evidence_type": "text_answer_ocr",
                "notes": "pure text answer page for VLM OCR",
            },
        ],
    },
    "exercise_53_53": {
        "image_path": "data/练习解答（图片）/练习53.png",
        "items": [
            {"exercise": 53, "subquestion": 1, "bbox": [30, 84, 870, 252]},
            {"exercise": 53, "subquestion": 2, "bbox": [30, 300, 870, 470]},
            {"exercise": 53, "subquestion": 3, "bbox": [30, 528, 870, 700]},
            {"exercise": 53, "subquestion": 4, "bbox": [30, 750, 870, 932]},
            {"exercise": 53, "subquestion": 5, "bbox": [30, 970, 870, 1142]},
            {"exercise": 53, "subquestion": 6, "bbox": [1000, 84, 1858, 252]},
            {"exercise": 53, "subquestion": 7, "bbox": [1000, 300, 1858, 470]},
            {"exercise": 53, "subquestion": 8, "bbox": [1000, 528, 1858, 700]},
            {"exercise": 53, "subquestion": 9, "bbox": [1000, 750, 1858, 932]},
            {"exercise": 53, "subquestion": 10, "bbox": [1000, 970, 1858, 1142]},
        ],
    },
    "exercise_54_54": {
        "image_path": "data/练习解答（图片）/练习54.png",
        "items": [
            {
                "exercise": 54,
                "subquestion": "all",
                "bbox": [0, 0, 1149, 678],
                "evidence_type": "text_answer_ocr",
                "notes": "pure text answer page for VLM OCR",
            },
        ],
    },
    "exercise_55_57": {
        "image_path": "data/练习解答（图片）/练习55-57.png",
        "items": [
            {"exercise": 55, "subquestion": 1, "bbox": [84, 140, 230, 412]},
            {"exercise": 55, "subquestion": 2, "bbox": [268, 140, 412, 412]},
            {"exercise": 55, "subquestion": 3, "bbox": [452, 140, 596, 412]},
            {"exercise": 55, "subquestion": 4, "bbox": [636, 140, 780, 412]},
            {"exercise": 55, "subquestion": 5, "bbox": [820, 140, 964, 412]},
            {"exercise": 56, "subquestion": 1, "bbox": [998, 140, 1154, 412]},
            {"exercise": 56, "subquestion": 2, "bbox": [1190, 140, 1340, 412]},
            {"exercise": 56, "subquestion": 3, "bbox": [1366, 140, 1525, 412]},
            {"exercise": 56, "subquestion": 4, "bbox": [1556, 140, 1706, 412]},
            {"exercise": 56, "subquestion": 5, "bbox": [1735, 140, 1885, 412]},
            {"exercise": 57, "subquestion": 1, "bbox": [88, 590, 242, 862]},
            {"exercise": 57, "subquestion": 2, "bbox": [268, 590, 426, 862]},
            {"exercise": 57, "subquestion": 3, "bbox": [452, 590, 608, 862]},
            {"exercise": 57, "subquestion": 4, "bbox": [636, 590, 792, 862]},
            {"exercise": 57, "subquestion": 5, "bbox": [820, 590, 975, 862]},
        ],
    },
    "exercise_58_59": {
        "image_path": "data/练习解答（图片）/练习58-59.png",
        "items": [
            {"exercise": 58, "subquestion": 1, "bbox": [8, 100, 138, 332]},
            {"exercise": 58, "subquestion": 2, "bbox": [175, 100, 292, 332]},
            {"exercise": 58, "subquestion": 3, "bbox": [337, 98, 446, 332]},
            {"exercise": 58, "subquestion": 4, "bbox": [475, 98, 606, 332]},
            {"exercise": 58, "subquestion": 5, "bbox": [640, 100, 760, 332]},
            {"exercise": 58, "subquestion": 6, "bbox": [790, 100, 900, 332]},
            {"exercise": 58, "subquestion": 7, "bbox": [930, 100, 1050, 332]},
            {"exercise": 58, "subquestion": 8, "bbox": [1100, 100, 1208, 332]},
            {"exercise": 58, "subquestion": 9, "bbox": [1248, 100, 1362, 332]},
            {"exercise": 58, "subquestion": 10, "bbox": [1408, 100, 1520, 332]},
            {"exercise": 59, "subquestion": 1, "bbox": [18, 480, 128, 710]},
            {"exercise": 59, "subquestion": 2, "bbox": [172, 480, 284, 710]},
            {"exercise": 59, "subquestion": 3, "bbox": [320, 480, 444, 710]},
            {"exercise": 59, "subquestion": 4, "bbox": [476, 480, 600, 710]},
            {"exercise": 59, "subquestion": 5, "bbox": [644, 480, 752, 710]},
            {"exercise": 59, "subquestion": 6, "bbox": [12, 780, 130, 1008]},
            {"exercise": 59, "subquestion": 7, "bbox": [166, 780, 292, 1008]},
            {"exercise": 59, "subquestion": 8, "bbox": [320, 780, 445, 1008]},
            {"exercise": 59, "subquestion": 9, "bbox": [480, 780, 602, 1008]},
            {"exercise": 59, "subquestion": 10, "bbox": [644, 780, 760, 1008]},
            {"exercise": 59, "subquestion": 11, "bbox": [15, 1074, 150, 1290]},
            {"exercise": 59, "subquestion": 12, "bbox": [170, 1074, 294, 1290]},
            {"exercise": 59, "subquestion": 13, "bbox": [322, 1074, 446, 1290]},
            {"exercise": 59, "subquestion": 14, "bbox": [480, 1074, 604, 1290]},
            {"exercise": 59, "subquestion": 15, "bbox": [640, 1074, 760, 1290]},
        ],
    },
}


def clamp_bbox(bbox: list[int], width: int, height: int) -> tuple[int, int, int, int]:
    x1, y1, x2, y2 = bbox
    return max(0, x1), max(0, y1), min(width, x2), min(height, y2)


def build_task(task_id: str) -> dict[str, Any]:
    layout = MANUAL_LAYOUTS[task_id]
    image_path = workspace_path(layout["image_path"])
    output_dir = OUTPUT_ROOT / task_id / "question_segments_v2"
    crop_dir = output_dir / "crops"
    crop_dir.mkdir(parents=True, exist_ok=True)

    image = Image.open(image_path).convert("RGB")
    width, height = image.size
    annotated = image.copy()
    draw = ImageDraw.Draw(annotated)

    items: list[dict[str, Any]] = []
    for index, raw_item in enumerate(layout["items"], start=1):
        x1, y1, x2, y2 = clamp_bbox(raw_item["bbox"], width, height)
        subquestion = raw_item["subquestion"]
        part_index = int(raw_item.get("part", 1))
        subquestion_slug = f"{subquestion:02d}" if isinstance(subquestion, int) else str(subquestion)
        part_suffix = f"_part{part_index}" if part_index != 1 else ""
        crop_name = f"exercise_{raw_item['exercise']:02d}_{subquestion_slug}{part_suffix}.png"
        crop_path = crop_dir / crop_name
        image.crop((x1, y1, x2, y2)).save(crop_path)

        item_id = f"qseg_{index:03d}"
        label = f"{item_id} E{raw_item['exercise']}-{raw_item['subquestion']}"
        color = (36, 120, 230)
        draw.rectangle((x1, y1, x2, y2), outline=color, width=4)
        label_box = (x1, max(0, y1 - 22), min(width, x1 + 168), y1)
        draw.rectangle(label_box, fill=color)
        draw.text((label_box[0] + 4, label_box[1] + 4), label, fill=(255, 255, 255))

        items.append(
            {
                "item_id": item_id,
                "exercise_number": raw_item["exercise"],
                "subquestion_number": subquestion,
                "part_index": part_index,
                "evidence_type": raw_item.get("evidence_type", "fretboard_diagram"),
                "bbox": {"x1": x1, "y1": y1, "x2": x2, "y2": y2},
                "crop_path": str(crop_path.relative_to(output_dir)).replace("\\", "/"),
                "source_image": rel_path(image_path),
                "review_status": "pending",
                "notes": raw_item.get("notes", "question-level crop includes prompt text and fretboard diagram"),
            }
        )

    annotated.save(output_dir / "annotated_question_segments.png")
    (output_dir / "question_segments.json").write_text(
        json.dumps({"task_id": task_id, "image_path": rel_path(image_path), "items": items}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    lines = [
        "# 题目完整块 v2 审核",
        "",
        f"- task_id: `{task_id}`",
        f"- source_image: `{rel_path(image_path)}`",
        "- segments_json: `question_segments.json`",
        "- annotated_image: `annotated_question_segments.png`",
        "",
        "## 标注总览",
        "",
        "![](annotated_question_segments.png)",
        "",
        "## 候选分块",
        "",
        "说明：这版裁切目标是一题一块，同时包含题号、文字说明和指板图。确认无误后把 accept 改成 `[x]`。",
        "",
        "| accept | item | exercise | subquestion | evidence_type | bbox | crop | notes |",
        "| --- | --- | ---: | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        bbox = item["bbox"]
        lines.append(
            f"| [ ] | `{item['item_id']}` | {item['exercise_number']} | {item['subquestion_number']} | "
            f"{item['evidence_type']} | {bbox['x1']},{bbox['y1']},{bbox['x2']},{bbox['y2']} | "
            f"![]({item['crop_path']}) | {item['notes']} |"
        )
    (output_dir / "question_segment_review.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    return {
        "task_id": task_id,
        "items": len(items),
        "output_dir": rel_path(output_dir),
        "review_md": rel_path(output_dir / "question_segment_review.md"),
        "annotated_image": rel_path(output_dir / "annotated_question_segments.png"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build question-level crops that include text and fretboard diagrams.")
    parser.add_argument("--task-id", choices=sorted(MANUAL_LAYOUTS), default="exercise_47_48")
    args = parser.parse_args()
    print(json.dumps(build_task(args.task_id), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
