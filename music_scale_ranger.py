import inspect
from music21 import scale, pitch, chord

"""possible_scales = [
        scale.MajorScale,
        scale.MinorScale,
        scale.DorianScale,
        scale.PhrygianScale,
        scale.LydianScale,
        scale.MixolydianScale,
        scale.LocrianScale,
        scale.HarmonicMinorScale,
        scale.MelodicMinorScale,
        scale.WeightedHexatonicBlues,
        BluesScale
    ]"""



# ==========================================
# 1. CLASSES E REGISTRO
# ==========================================

class BluesScale(scale.Scale):
    """Escala de Blues adaptada para funcionar passivamente em buscas."""
    def __init__(self, tonic='C4'):
        super().__init__()
        self.tonic = pitch.Pitch(tonic)
        self.intervals = ['P1', 'm3', 'P4', 'd5', 'P5', 'm7']

    def getPitches(self, minPitch=None, maxPitch=None):
        p_min = pitch.Pitch(minPitch) if minPitch else pitch.Pitch('C0')
        p_max = pitch.Pitch(maxPitch) if maxPitch else pitch.Pitch('C8')
        
        pitches = []
        for octv in range(p_min.octave - 1, p_max.octave + 2):
            base_tonic = pitch.Pitch(self.tonic.name)
            base_tonic.octave = octv
            for i in self.intervals:
                p = base_tonic.transpose(i)
                if p_min.ps <= p.ps <= p_max.ps:
                    pitches.append(p)
        return pitches


REGISTRO_ESCALAS = {
    'MajorScale': scale.MajorScale,
    'MinorScale': scale.MinorScale,
    'HarmonicMinorScale': scale.HarmonicMinorScale,
    'MelodicMinorScale': scale.MelodicMinorScale,
    'BluesScale': BluesScale
}

# ==========================================
# 2. GERAÇÃO DE CAMPO HARMÔNICO (COM TRAVA TEÓRICA)
# ==========================================

def enharmonic_equal(note1, note2) -> bool:
    """Retorna True se duas notas são enarmônicas (ex: C# == Db)."""
    p1 = pitch.Pitch(note1)
    p2 = pitch.Pitch(note2)
    return p1.name == p2.name or p1.getEnharmonic().name == p2.name or p2.getEnharmonic().name == p1.name


def guess_scales_from_notes(notes_list: list) -> list:
    """Retorna uma lista de strings com as escalas compatíveis com as notas informadas."""
    possible_scales = [
        scale.MajorScale, scale.MinorScale, scale.DorianScale,
        scale.PhrygianScale, scale.LydianScale, scale.MixolydianScale,
        scale.LocrianScale, scale.HarmonicMinorScale, scale.MelodicMinorScale,
        scale.WeightedHexatonicBlues, BluesScale
    ]
    
    results = []
    tonics = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    for sc in possible_scales:
        for tonic in tonics:
            s = sc(tonic)
            scale_notes = [p.getEnharmonic().name for p in s.getPitches(tonic+'0', tonic+'7')]
            
            if all(any(enharmonic_equal(n, sn) for sn in scale_notes) for n in notes_list):
                results.append(f"{sc.__name__} com tônica {tonic}")
                
    return results


def get_scale_notes(escala_nome: str, tonalidade: str) -> list:
    """Retorna as notas de uma escala dada a sua classe e tônica."""
    # PATCH: Força o código a enxergar a classe local antes do getattr
    if escala_nome == 'BluesScale':
        escala_class = BluesScale
    else:
        escala_class = getattr(scale, escala_nome)
        
    s = escala_class(tonalidade)
    scale_notes = s.getPitches(tonalidade+'3', tonalidade+'4')
    return [p.name for p in scale_notes]

def get_harmonic_field(escala_nome: str, tonalidade: str, seventh: bool) -> list:
    """Gera campo harmônico estritamente para escalas diatônicas de 7 notas, incluindo as notas do acorde."""
    if escala_nome not in REGISTRO_ESCALAS:
        raise AttributeError(f"Escala '{escala_nome}' não registrada.")
        
    s = REGISTRO_ESCALAS[escala_nome](tonalidade)
    
    # Extrai apenas as notas de uma oitava para avaliar a estrutura teórica
    uma_oitava = s.getPitches(tonalidade+'4', tonalidade+'5')
    notas_unicas = len({p.pitchClass for p in uma_oitava})
    
    # TRAVA TEÓRICA: Impede a geração de acordes sobrepostos em escalas não-diatônicas
    if notas_unicas != 7:
        raise ValueError(
            f"Erro Teórico: A escala '{escala_nome}' tem {notas_unicas} notas. "
            "Campos harmônicos tradicionais exigem escalas heptatônicas (7 notas) "
            "para o empilhamento correto de terças."
        )
    
    # Se passou na trava, busca 3 oitavas para empilhar os acordes em segurança
    scale_notes = s.getPitches(tonalidade+'3', tonalidade+'6')
    
    chords = []
    # Loop fixo de 1 a 7 (graus diatônicos)
    for degree in range(1, 8):
        idx = degree - 1
        
        # Empilha Tônica, 3ª e 5ª diatônicas
        chord_pitches = [scale_notes[idx], scale_notes[idx+2], scale_notes[idx+4]]
        
        # Adiciona a 7ª se solicitado
        if seventh:
            chord_pitches.append(scale_notes[idx+6])
            
        acorde = chord.Chord(chord_pitches)
        
        # Extrai o nome de cada nota formadora do acorde e junta com vírgulas
        notas_acorde = ", ".join([p.name for p in acorde.pitches])
        
        # Passa a retornar uma tupla com 3 elementos
        chords.append((degree, acorde.pitchedCommonName, notas_acorde))
            
    return chords

# ==========================================
# 3. INTERFACE DE EXECUÇÃO (CLI)
# ==========================================

def menu_interativo():
    while True:
        print("\n" + "="*40)
        print("MÓDULO DE ANÁLISE MUSICAL".center(40))
        print("="*40)
        print("1. Descobrir escalas a partir de notas")
        print("2. Ver notas de uma escala específica")
        print("3. Ver campo harmônico (tríades/tétrades)")
        print("4. Sair")
        print("="*40)
        
        escolha = input("Escolha uma opção (1-4): ").strip()
        
        if escolha == '1':
            entrada = input("\nDigite as notas separadas por espaço (ex: C E G): ")
            notas = entrada.strip().split()
            res = guess_scales_from_notes(notas)
            if res:
                print("\nEscalas possíveis (enarmonia ignorada):")
                for r in res:
                    print("-", r)
            else:
                print("\nNenhuma escala compatível encontrada.")
                
        elif escolha == '2':
            escala_nome = input('\nDigite o nome da escala (ex: MajorScale, MinorScale, HarmonicMinorScale, MelodicMinorScale, BluesScale, WeightedHexatonicBlues): ').strip()
            tonalidade = input('Digite a tônica (ex: C, D#, Bb): ').strip()
            try:
                notas = get_scale_notes(escala_nome, tonalidade)
                print(f"\nNotas da escala {escala_nome} com tônica {tonalidade}:")
                print(" - ".join(notas))
            except AttributeError:
                print("\n[Erro] Essa escala não existe na biblioteca music21.")
                
        elif escolha == '3':
                    escala_nome = input('\nDigite o nome da escala (ex: MajorScale, MinorScale, HarmonicMinorScale, MelodicMinorScale, BluesScale, WeightedHexatonicBlues): ').strip()
                    tonalidade = input('Digite a tônica (ex: C, D#, F#): ').strip()
                    tipo = input('Você quer acordes tétrades ou tríades? Digite 4 ou 3: ').strip()
                    
                    seventh = (tipo == '4')
                    try:
                        chords = get_harmonic_field(escala_nome, tonalidade, seventh)
                        tipo_str = 'tétrades' if seventh else 'tríades'
                        print(f"\nCampo harmônico de {escala_nome} com tônica {tonalidade} ({tipo_str}):")
                        
                        # Desempacota os 3 valores agora retornados pela função
                        for degree, name, notas in chords:
                            print(f"Grau {degree}: {name} ({notas})")
                            
                    except AttributeError:
                        print("\n[Erro] Essa escala não existe na biblioteca music21.")
                    except ValueError as e:
                        print(f"\n[Erro] {e}")
                
        elif escolha == '4':
            print("\nEncerrando o programa...")
            break
            
        else:
            print("\n[Erro] Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu_interativo()