with open(r'F:\kicad\share\kicad\symbols\power.kicad_sym', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's find symbol "PWR_FLAG"
start_idx = content.find('(symbol "PWR_FLAG"')
if start_idx != -1:
    # Find matching closing parenthesis
    depth = 0
    end_idx = start_idx
    for i, char in enumerate(content[start_idx:]):
        if char == '(':
            depth += 1
        elif char == ')':
            depth -= 1
            if depth == 0:
                end_idx = start_idx + i + 1
                break
    pwr_flag_sym = content[start_idx:end_idx]
    print("Found PWR_FLAG symbol definition length:", len(pwr_flag_sym))
    with open('pwr_flag_def.txt', 'w', encoding='utf-8') as out:
        out.write(pwr_flag_sym)
else:
    print("PWR_FLAG not found in power.kicad_sym")
