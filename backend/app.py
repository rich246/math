from flask import Flask, request, jsonify
from flask_cors import CORS
import sympy as sp

app = Flask(__name__)
CORS(app)

# 简单工具：尝试把字符串转为 sympy 表达式
def parse_expr(expr_str):
    try:
        expr = sp.sympify(expr_str)
        return expr, None
    except Exception as e:
        return None, str(e)

@app.route('/api/solve', methods=['POST'])
def solve_endpoint():
    data = request.get_json() or {}
    mode = data.get('mode', 'simplify')
    expr_str = data.get('expr', '')
    var = data.get('var', None)  # 可选的求解变量

    if not expr_str:
        return jsonify({'error': 'expr 不能为空'}), 400

    # 解析表达式（或等式）
    try:
        # 若包含等号，拆分为左右两侧
        if '=' in expr_str:
            left_s, right_s = expr_str.split('=', 1)
            left, err = parse_expr(left_s)
            if err: raise ValueError(err)
            right, err = parse_expr(right_s)
            if err: raise ValueError(err)
            expr = sp.Eq(left, right)
        else:
            expr, err = parse_expr(expr_str)
            if err: raise ValueError(err)
    except Exception as e:
        return jsonify({'error': '解析表达式失败: ' + str(e)}), 400

    try:
        if mode == 'simplify':
            steps = [
                {'step': '原始表达式', 'latex': sp.latex(expr)},
            ]
            simplified = sp.simplify(expr)
            steps.append({'step': '化简后', 'latex': sp.latex(simplified)})
            return jsonify({'mode': mode, 'result_latex': sp.latex(simplified), 'steps': steps})

        elif mode == 'solve':
            # 若传入等式，使用 Eq；否则对表达式等于0 求解
            if isinstance(expr, sp.Equality) or isinstance(expr, sp.Eq):
                equation = expr
            else:
                # expression assumed equals zero
                equation = sp.Eq(expr, 0)

            if var:
                symbol = sp.Symbol(var)
            else:
                # 试图自动选取未知量
                free = list(sp.sympify(expr_str).free_symbols)
                if len(free) == 0:
                    return jsonify({'error': '未指定未知量，且表达式中未找到符号'}), 400
                symbol = free[0]

            sol = sp.solve(equation, symbol)
            steps = [
                {'step': '方程', 'latex': sp.latex(equation)},
                {'step': '求解结果', 'latex': sp.latex(sol)}
            ]
            return jsonify({'mode': mode, 'result_latex': sp.latex(sol), 'steps': steps})

        elif mode == 'diff' or mode == 'derivative':
            if var:
                symbol = sp.Symbol(var)
            else:
                free = list(expr.free_symbols)
                if len(free) == 0:
                    return jsonify({'error': '未找到变量，请传入 var 字段'}), 400
                symbol = free[0]
            derivative = sp.diff(expr, symbol)
            steps = [
                {'step': '被微分函数', 'latex': sp.latex(expr)},
                {'step': '求导结果', 'latex': sp.latex(derivative)}
            ]
            return jsonify({'mode': mode, 'result_latex': sp.latex(derivative), 'steps': steps})

        elif mode == 'integrate':
            if var:
                symbol = sp.Symbol(var)
            else:
                free = list(expr.free_symbols)
                if len(free) == 0:
                    return jsonify({'error': '未找到变量，请传入 var 字段'}), 400
                symbol = free[0]
            integral = sp.integrate(expr, symbol)
            steps = [
                {'step': '被积函数', 'latex': sp.latex(expr)},
                {'step': '不定积分', 'latex': sp.latex(integral)}
            ]
            return jsonify({'mode': mode, 'result_latex': sp.latex(integral), 'steps': steps})

        else:
            return jsonify({'error': '不支持的 mode: ' + str(mode)}), 400

    except Exception as e:
        return jsonify({'error': '计算失败: ' + str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
