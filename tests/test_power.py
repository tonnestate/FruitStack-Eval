import pytest

from fruitstack_eval.power import paired_noninferiority_n, unpaired_noninferiority_n


@pytest.mark.parametrize("margin,psi,expected", [(0.10, 0.2, 157), (0.10, 0.3, 236), (0.05, 0.2, 628), (0.05, 0.3, 942)])
def test_paired_table_matches_protocol(margin, psi, expected):
    assert paired_noninferiority_n(margin, psi) == expected


def test_unpaired_matches_protocol():
    assert unpaired_noninferiority_n(0.05, 0.7) == 1319
    assert unpaired_noninferiority_n(0.10, 0.7) == 330


def test_true_advantage_reduces_sample_size():
    assert paired_noninferiority_n(0.05, 0.2, true_difference=0.05) < paired_noninferiority_n(0.05, 0.2)


@pytest.mark.parametrize("kwargs", [{"margin": 0.0, "discordance": 0.2}, {"margin": 0.1, "discordance": 0.0},
                                    {"margin": 0.1, "discordance": 0.2, "alpha": 0.6},
                                    {"margin": 0.1, "discordance": 0.2, "true_difference": -0.2}])
def test_invalid_inputs_rejected(kwargs):
    with pytest.raises(ValueError):
        paired_noninferiority_n(**kwargs)
