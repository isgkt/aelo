use proptest::prelude::*;

#[test]
fn sum_test() {
    assert_eq!(5 + 3, 8);
}

proptest! {
    #[test]
    fn pb_sum_test(
        left in 0..1000i32,
        right in 0..1000i32
    ) {
        assert_eq!(left + right, right + left);
    }
}
