#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Tests for Matlab code generator

"""

import pytest

from PyDSTool import FuncSpec


def test_matlab_funcspec_for_ds_with_single_var_and_single_param():
    args = {
        'name': 'fun_with_var_and_par',
        'targetlang': 'matlab',
        'vars': ['x'],
        'pars': ['p'],
        'varspecs': {'x': 'p * x - 1'},
        'fnspecs': {'myaux': (['x'], 'x**2 + p')},
    }
    fs = FuncSpec(args)
    assert fs.spec[0].split('\n') == [
        'function [vf_, y_] = vfield(vf_, t_, x_, p_)',
        '% Vector field definition for model fun_with_var_and_par',
        '% Generated by PyDSTool for ADMC++ target',
        '',
        '',
        '% Parameter definitions',
        '',
        '\tp = p_(1);',
        '',
        '% Variable definitions',
        '',
        '\tx = x_(1);',
        '',
        '',
        'y_(1) = p * x - 1;',
        '',
        '',
        '',
    ]

    assert fs.auxfns['myaux'][0].split('\n') == [
        'function y_ = myaux(x__,  p_)',
        '% Auxilliary function myaux for model fun_with_var_and_par',
        '% Generated by PyDSTool for ADMC++ target',
        '',
        '',
        '% Parameter definitions',
        '',
        '\tp = p_(1);',
        ' ',
        '',
        '',
        'y_ = x__^2+p;',
        '',
        ''
    ]

    assert all(fn in fs._pyauxfns.keys() for fn in [
        'getbound',
        'getindex',
        'globalindepvar',
        'heav',
        'if',
        'initcond',
    ])

    assert 'myaux' in fs._pyauxfns.keys()


def test_matlab_funspec_for_macro_raises_exception():
    with pytest.raises(ValueError):
        FuncSpec({
            'vars': ['z1', 'z2', 'z3'],
            'targetlang': 'matlab',
            'varspecs': {
                'z[i]': 'for(i, 1, 3, z[i]**2)',
            },
        })


def test_matlab_funspec_if_raises_exception():
    with pytest.raises(NotImplementedError):
        FuncSpec({
            'name': 'single_var',
            'targetlang': 'matlab',
            'vars': ['x'],
            'varspecs': {'x': 'if(x < 0, x, x**3)'},
        })


def test_matlab_funcspec_has_python_user_auxfn_interface():
    args = {
        'name': 'test_user_auxfn_interface',
        'targetlang': 'matlab',
        'vars': ['x'],
        'pars': ['p'],
        'varspecs': {'x': 'p * x - 1'},
        'fnspecs': {'myaux': (['x'], 'x**2 + p')},
    }
    fs = FuncSpec(args)

    assert fs._user_auxfn_interface['myaux'].split('\n') == [
        'def myaux(self,x,__parsinps__=None):',
        '\tif __parsinps__ is None:',
        '\t\t__parsinps__=self.map_ixs(self.genref)',
        '\treturn self.genref._auxfn_myaux(__parsinps__,x)',
        ''
    ]


def test_matlab_funcspec_inserts_additional_code_in_vfield():
    start = 'disp("START");'
    end = 'disp("END");'
    args = {
        'name': 'test_codeinsert',
        'targetlang': 'matlab',
        'vars': ['x'],
        'pars': ['p'],
        'varspecs': {'x': 'p * x - 1'},
        'fnspecs': {'myaux': (['x'], 'x**2 + p')},
        'codeinsert_start': start,
        'codeinsert_end': end,
    }
    fs = FuncSpec(args)
    assert fs.spec[0].split('\n') == [
        'function [vf_, y_] = vfield(vf_, t_, x_, p_)',
        '% Vector field definition for model test_codeinsert',
        '% Generated by PyDSTool for ADMC++ target',
        '',
        '',
        '% Parameter definitions',
        '',
        '\tp = p_(1);',
        '',
        '% Variable definitions',
        '',
        '\tx = x_(1);',
        '',
        '% Verbose code insert -- begin ',
        start,
        '% Verbose code insert -- end ',
        '',
        '',
        'y_(1) = p * x - 1;',
        '',
        '% Verbose code insert -- begin ',
        end,
        '% Verbose code insert -- end ',
        '',
        '',
        '',
    ]

    assert fs.auxfns['myaux'][0].split('\n') == [
        'function y_ = myaux(x__,  p_)',
        '% Auxilliary function myaux for model test_codeinsert',
        '% Generated by PyDSTool for ADMC++ target',
        '',
        '',
        '% Parameter definitions',
        '',
        '\tp = p_(1);',
        ' ',
        '',
        '',
        'y_ = x__^2+p;',
        '',
        ''
    ]

    assert all(fn in fs._pyauxfns.keys() for fn in [
        'getbound',
        'getindex',
        'globalindepvar',
        'heav',
        'if',
        'initcond',
    ])

    assert 'myaux' in fs._pyauxfns.keys()
