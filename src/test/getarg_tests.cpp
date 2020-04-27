#include <boost/algorithm/string.hpp>
#include <boost/foreach.hpp>
#include <boost/test/unit_test.hpp>

#include "util.h"

BOOST_AUTO_TEST_SUITE(getarg_tests)

static void
ResetArgs(const std::string& strArg)
{
    std::vector<std::string> vecArg;
    boost::split(vecArg, strArg, boost::is_space(), boost::token_compress_on);

    // Insert dummy executable name:
    vecArg.insert(vecArg.begin(), "testbitcoin");

    // Convert to char*:
    std::vector<const char*> vecChar;
    BOOST_FOREACH(std::string& s, vecArg)
        vecChar.push_back(s.c_str());

    ParseParameters(vecChar.size(), &vecChar[0]);
}

BOOST_AUTO_TEST_CASE(boolarg)
{
    ResetArgs("-rec");
    BOOST_CHECK(GetBoolArg("-rec"));
    BOOST_CHECK(GetBoolArg("-rec", false));
    BOOST_CHECK(GetBoolArg("-rec", true));

    BOOST_CHECK(!GetBoolArg("-fo"));
    BOOST_CHECK(!GetBoolArg("-fo", false));
    BOOST_CHECK(GetBoolArg("-fo", true));

    BOOST_CHECK(!GetBoolArg("-reco"));
    BOOST_CHECK(!GetBoolArg("-reco", false));
    BOOST_CHECK(GetBoolArg("-reco", true));

    ResetArgs("-rec=0");
    BOOST_CHECK(!GetBoolArg("-rec"));
    BOOST_CHECK(!GetBoolArg("-rec", false));
    BOOST_CHECK(!GetBoolArg("-rec", true));

    ResetArgs("-rec=1");
    BOOST_CHECK(GetBoolArg("-rec"));
    BOOST_CHECK(GetBoolArg("-rec", false));
    BOOST_CHECK(GetBoolArg("-rec", true));

    // New 0.6 feature: auto-map -nosomething to !-something:
    ResetArgs("-norec");
    BOOST_CHECK(!GetBoolArg("-rec"));
    BOOST_CHECK(!GetBoolArg("-rec", false));
    BOOST_CHECK(!GetBoolArg("-rec", true));

    ResetArgs("-norec=1");
    BOOST_CHECK(!GetBoolArg("-rec"));
    BOOST_CHECK(!GetBoolArg("-rec", false));
    BOOST_CHECK(!GetBoolArg("-rec", true));

    ResetArgs("-rec -norec");  // -rec should win
    BOOST_CHECK(GetBoolArg("-rec"));
    BOOST_CHECK(GetBoolArg("-rec", false));
    BOOST_CHECK(GetBoolArg("-rec", true));

    ResetArgs("-rec=1 -norec=1");  // -rec should win
    BOOST_CHECK(GetBoolArg("-rec"));
    BOOST_CHECK(GetBoolArg("-rec", false));
    BOOST_CHECK(GetBoolArg("-rec", true));

    ResetArgs("-rec=0 -norec=0");  // -rec should win
    BOOST_CHECK(!GetBoolArg("-rec"));
    BOOST_CHECK(!GetBoolArg("-rec", false));
    BOOST_CHECK(!GetBoolArg("-rec", true));

    // New 0.6 feature: treat -- same as -:
    ResetArgs("--rec=1");
    BOOST_CHECK(GetBoolArg("-rec"));
    BOOST_CHECK(GetBoolArg("-rec", false));
    BOOST_CHECK(GetBoolArg("-rec", true));

    ResetArgs("--norec=1");
    BOOST_CHECK(!GetBoolArg("-rec"));
    BOOST_CHECK(!GetBoolArg("-rec", false));
    BOOST_CHECK(!GetBoolArg("-rec", true));

}

BOOST_AUTO_TEST_CASE(stringarg)
{
    ResetArgs("");
    BOOST_CHECK_EQUAL(GetArg("-rec", ""), "");
    BOOST_CHECK_EQUAL(GetArg("-rec", "eleven"), "eleven");

    ResetArgs("-rec -bar");
    BOOST_CHECK_EQUAL(GetArg("-rec", ""), "");
    BOOST_CHECK_EQUAL(GetArg("-rec", "eleven"), "");

    ResetArgs("-rec=");
    BOOST_CHECK_EQUAL(GetArg("-rec", ""), "");
    BOOST_CHECK_EQUAL(GetArg("-rec", "eleven"), "");

    ResetArgs("-rec=11");
    BOOST_CHECK_EQUAL(GetArg("-rec", ""), "11");
    BOOST_CHECK_EQUAL(GetArg("-rec", "eleven"), "11");

    ResetArgs("-rec=eleven");
    BOOST_CHECK_EQUAL(GetArg("-rec", ""), "eleven");
    BOOST_CHECK_EQUAL(GetArg("-rec", "eleven"), "eleven");

}

BOOST_AUTO_TEST_CASE(intarg)
{
    ResetArgs("");
    BOOST_CHECK_EQUAL(GetArg("-rec", 11), 11);
    BOOST_CHECK_EQUAL(GetArg("-rec", 0), 0);

    ResetArgs("-rec -bar");
    BOOST_CHECK_EQUAL(GetArg("-rec", 11), 0);
    BOOST_CHECK_EQUAL(GetArg("-bar", 11), 0);

    ResetArgs("-rec=11 -bar=12");
    BOOST_CHECK_EQUAL(GetArg("-rec", 0), 11);
    BOOST_CHECK_EQUAL(GetArg("-bar", 11), 12);

    ResetArgs("-rec=NaN -bar=NotANumber");
    BOOST_CHECK_EQUAL(GetArg("-rec", 1), 0);
    BOOST_CHECK_EQUAL(GetArg("-bar", 11), 0);
}

BOOST_AUTO_TEST_CASE(doubledash)
{
    ResetArgs("--rec");
    BOOST_CHECK_EQUAL(GetBoolArg("-rec"), true);

    ResetArgs("--rec=verbose --bar=1");
    BOOST_CHECK_EQUAL(GetArg("-rec", ""), "verbose");
    BOOST_CHECK_EQUAL(GetArg("-bar", 0), 1);
}

BOOST_AUTO_TEST_CASE(boolargno)
{
    ResetArgs("-norec");
    BOOST_CHECK(!GetBoolArg("-rec"));
    BOOST_CHECK(!GetBoolArg("-rec", true));
    BOOST_CHECK(!GetBoolArg("-rec", false));

    ResetArgs("-norec=1");
    BOOST_CHECK(!GetBoolArg("-rec"));
    BOOST_CHECK(!GetBoolArg("-rec", true));
    BOOST_CHECK(!GetBoolArg("-rec", false));

    ResetArgs("-norec=0");
    BOOST_CHECK(GetBoolArg("-rec"));
    BOOST_CHECK(GetBoolArg("-rec", true));
    BOOST_CHECK(GetBoolArg("-rec", false));

    ResetArgs("-rec --norec");
    BOOST_CHECK(GetBoolArg("-rec"));

    ResetArgs("-norec -rec"); // rec always wins:
    BOOST_CHECK(GetBoolArg("-rec"));
}

BOOST_AUTO_TEST_SUITE_END()
