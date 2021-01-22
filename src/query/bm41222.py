from data import *
from generate.angular_separation import EclipticPosition
from generate.planet_events import InnerPlanetPhenomena
from query.database import BabylonianDay
from query.result import PlanetaryEventResult, SearchRange, AngularSeparationResult, AbstractResult
from query.tablet import AbstractTablet, PotentialMonthResult, MultiyearResult, YearToTest


class BM41222(AbstractTablet):

    ## Shamash-shum-ukin

    def shamash_14_xii(self, month: List[BabylonianDay]) -> List[AbstractResult]:
        day4 = SearchRange.for_night(month, 4)
        # Mercury's first appearance in the west
        res1 = PlanetaryEventResult(self.db, MERCURY, InnerPlanetPhenomena.EF, day4)
        # in the area of the Swallow.
        res2 = AngularSeparationResult(self.db, MERCURY, PISCES.central_star, 0, PISCES.radius, None, day4)
        return [res1, res2]

    def shamash_year_14(self, nisan_1: float) -> List[PotentialMonthResult]:
        res1 = self.repeat_month_with_alternate_starts(nisan_1, 12, "Year 14 XII", self.shamash_14_xii)
        return [res1]


    def shamash_17_ii(self, month: List[BabylonianDay]) -> List[AbstractResult]:
        day19 = SearchRange.for_night(month, 19)
        # mars was in [the area?] of the Old Man
        res1 = AngularSeparationResult(self.db, MARS, PERSEUS.central_star, 0, PERSEUS.radius, None, day19)
        # to the right of Mercury
        res2 = AngularSeparationResult(self.db, MARS, MERCURY, 0, 30, EclipticPosition.AHEAD, day19)
        return [res1, res2]

    def shamash_year_17(self, nisan_1: float) -> List[PotentialMonthResult]:
        res1 = self.repeat_month_with_alternate_starts(nisan_1, 2, "Year 17 II", self.shamash_17_ii)
        return [res1]


    def shamash_19_vii(self, month: List[BabylonianDay]) -> List[AbstractResult]:
        day4 = SearchRange.for_night(month, 4)
        # Mercury stood for ⅔ cubit above? Mars
        res1 = AngularSeparationResult(self.db, MERCURY, MARS, (2/3 * CUBIT), 1 * CUBIT, EclipticPosition.ABOVE, day4)
        return [res1]

    def shamash_year_19(self, nisan_1: float) -> List[PotentialMonthResult]:
        res1 = self.repeat_month_with_alternate_starts(nisan_1, 7, "Year 19 VII", self.shamash_19_vii)
        return [res1]


    ## Kandalanu

    def kand_1_iii(self, month: List[BabylonianDay]) -> List[AbstractResult]:
        day28 = SearchRange.for_night(month, 28)
        # Mercury was in the back of Mars?
        res1 = AngularSeparationResult(self.db, MERCURY, MARS, 0, 30, EclipticPosition.BEHIND, day28)
        return [res1]

    def kand_year_1(self, nisan_1: float) -> List[PotentialMonthResult]:
        res1 = self.repeat_month_with_alternate_starts(nisan_1, 3, "Year 1 III", self.kand_1_iii)
        return [res1]


    def kand_12_i(self, month: List[BabylonianDay]) -> List[AbstractResult]:
        day8 = SearchRange.for_night(month, 8)
        # Mercury, in the area of Pleiades
        res1 = AngularSeparationResult(self.db, MERCURY, ALCYONE, 0, 10, None, day8)
        # Mercury was 2 ⅔ cubits above? Mars?
        res2 = AngularSeparationResult(self.db, MERCURY, MARS, (2 + 2/3) * CUBIT, 2 * CUBIT, EclipticPosition.ABOVE, day8)
        return [res1, res2]

    def kand_year_12(self, nisan_1: float) -> List[PotentialMonthResult]:
        res1 = self.repeat_month_with_alternate_starts(nisan_1, 1, "Year 12 I", self.kand_12_i)
        return [res1]


    def kand_16_iii(self, month: List[BabylonianDay]) -> List[AbstractResult]:
        day20 = SearchRange.for_night(month, 20)
        # Mercury stood 1 cubit 4 fingers behind Mars.
        res1 = AngularSeparationResult(self.db, MERCURY, MARS, (1 * CUBIT + 4 * FINGER), 1 * CUBIT, EclipticPosition.BEHIND, day20)
        return [res1]

    def kand_year_16(self, nisan_1: float) -> List[PotentialMonthResult]:
        res1 = self.repeat_month_with_alternate_starts(nisan_1, 3, "Year 16 III", self.kand_16_iii)
        return [res1]

    # Nabopolassar

    def nabo_7_unknown(self, month: List[BabylonianDay]) -> List[AbstractResult]:
        range = SearchRange(month[0].sunset, month[29].sunrise, "Unknown day")
        # Mercury was balanced 6 fingers above Mars.
        res1 = AngularSeparationResult(self.db, MERCURY, MARS, 6 * FINGER, 6 * FINGER, EclipticPosition.ABOVE, range)
        return [res1]

    def nabo_year_7(self, nisan_1: float) -> List[PotentialMonthResult]:
        attempts = []
        for m in range(1, 13):
            attempts.append(self.repeat_month_with_alternate_starts(nisan_1, m, "Year 7 ?", self.nabo_7_unknown))
        attempts.sort(key=lambda x: x.score, reverse=True)
        return attempts[:1]


    def nabo_12_iv(self, month: List[BabylonianDay]) -> List[AbstractResult]:
        day18 = SearchRange.for_night(month, 18)
        # Mars was with Pleiades
        res1 = AngularSeparationResult(self.db, MARS, ALCYONE, 0, 10, None, day18)
        return [res1]

    def nabo_12_vi(self, month: List[BabylonianDay]) -> List[AbstractResult]:
        day13 = SearchRange.for_night(month, 13)
        # Mars was ⅔ cubit above the Chariot
        res1 = AngularSeparationResult(self.db, MARS, AURIGA.central_star, 0, AURIGA.radius, None, day13)
        return [res1]

    def nabo_year_12(self, nisan_1: float) -> List[PotentialMonthResult]:
        iv = self.repeat_month_with_alternate_starts(nisan_1, 4, "Year 12 IV", self.nabo_12_iv)
        vi = self.repeat_month_with_alternate_starts(nisan_1, 6, "Year 12 VI", self.nabo_12_vi)
        return [iv, vi]


    def nabo_13_iii(self, month: List[BabylonianDay]) -> List[AbstractResult]:
        day1 = SearchRange.for_night(month, 1)
        # Mars was [....] above α Leonis.
        res1 = AngularSeparationResult(self.db, MARS, REGULUS, 0, 20, EclipticPosition.ABOVE, day1)
        return [res1]

    def nabo_13_v(self, month: List[BabylonianDay]) -> List[AbstractResult]:
        day3 = SearchRange.for_night(month, 3)
        # Mars ... it was with β Virginis
        res1 = AngularSeparationResult(self.db, MARS, BETA_VIRGINIS, 0, 10, None, day3)
        return [res1]

    def nabo_year_13(self, nisan_1: float) -> List[PotentialMonthResult]:
        iii = self.repeat_month_with_alternate_starts(nisan_1, 3, "Year 13 III", self.nabo_13_iii)
        v = self.repeat_month_with_alternate_starts(nisan_1, 5, "Year 13 V", self.nabo_13_v)
        return [iii, v]

    def do_query(self, subquery: Union[str, None], print_year: Union[int, None]):

        if subquery is not None:

            if subquery == "shamash":
                tests = [YearToTest(0, "Shamash-shum-ukin 14", self.shamash_year_14),
                         YearToTest(3, "Shamash-shum-ukin 17", self.shamash_year_17),
                         YearToTest(5, "Shamash-shum-ukin 19", self.shamash_year_19)]
                res = self.run_years(tests)
                self.print_results(res, "Shamash-shum-ukin year 14")

            elif subquery == "kandalanu":
                tests = [YearToTest(0, "Kanalanu 1", self.kand_year_1),
                         YearToTest(11, "Kanalanu 12", self.kand_year_12),
                         YearToTest(15, "Kanalanu 16", self.kand_year_16)]
                res = self.run_years(tests)
                self.print_results(res, "Kandalanu year 1")

            elif subquery == "nabopolassar":
                tests = [YearToTest(0, "Nabopolassar 7", self.nabo_year_7),
                         YearToTest(5, "Nabopolassar 12", self.nabo_year_12),
                         YearToTest(6, "Nabopolassar 13", self.nabo_year_13)]
                res = self.run_years(tests)
                self.print_results(res, "Nabopolassar year 7")

            else:
                raise RuntimeError("Please specify a valid subquery for this tablet")

        else:
            tests = [YearToTest(0, "Shamash-shum-ukin 14", self.shamash_year_14),
                     YearToTest(3, "Shamash-shum-ukin 17", self.shamash_year_17),
                     YearToTest(5, "Shamash-shum-ukin 19", self.shamash_year_19),
                     YearToTest(7, "Kanalanu 1", self.kand_year_1),
                     YearToTest(18, "Kanalanu 12", self.kand_year_12),
                     YearToTest(22, "Kanalanu 16", self.kand_year_16),
                     YearToTest(35, "Nabopolassar 7", self.nabo_year_7),
                     YearToTest(40, "Nabopolassar 12", self.nabo_year_12),
                     YearToTest(41, "Nabopolassar 13", self.nabo_year_13)]
            res = self.run_years(tests)
            self.print_results(res, "Shamash-shum-ukin year 14 to Nabopolassar (assuming reigns of 20, and 22)")

        self.output_json_for_year(res, print_year)


