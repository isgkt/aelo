use proptest::prelude::*;

#[test]
fn sumTest()
{
    assert_eq!(5 + 3, 8);
}

proptest! {
    #[test]
    fn pbSumTest(left in 0..1000i32, right in 0..1000i32)
    {
        assert_eq!(left + right, right + left);
    }
}