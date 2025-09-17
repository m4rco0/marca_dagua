import os
import re
import cv2
import rawpy


def ler_img_cr2(caminho_cr2_image):
    """
    Lê uma imagem no formato CR2 e a converte para o formato do OpenCV (BGR).

    Args:
        caminho_cr2_image (str): O caminho completo para o arquivo .CR2.

    Returns:
        np.array: A imagem em formato BGR, ou None se ocorrer um erro.
    """
    try:
        with rawpy.imread(caminho_cr2_image) as raw:
            image_rgb = raw.postprocess()
            image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
            return image_bgr
    except Exception as e:
        print(f"    -> Erro ao ler o arquivo CR2 '{caminho_cr2_image}': {e}")
        return None


def aplicar_marca_dagua(imagem, logo, opacidade=0.3, escala=0.4):
    """
    Aplica uma imagem de logo como marca d'água com opacidade geral.
    Esta versão é mais robusta e garante que os tamanhos da ROI e do logo sempre correspondam.

    Args:
        imagem (np.array): A imagem principal (fundo).
        logo (np.array): A imagem da marca d'água.
        opacidade (float): Nível de opacidade da marca d'água (0.0 a 1.0).
        escala (float): Fator para redimensionar o logo em relação à largura da imagem.

    Returns:
        np.array: A imagem com a marca d'água aplicada.
    """
    if imagem is None or logo is None:
        print("Erro: Imagem principal ou logo não carregados.")
        return None



    h_imagem, w_imagem, _ = imagem.shape

    # Redimensiona o logo UMA VEZ para ter uma base de tamanho
    base_w_logo = int(w_imagem * escala)
    aspect_ratio = logo.shape[0] / logo.shape[1]
    base_h_logo = int(base_w_logo * aspect_ratio)
    
    # Calcula as coordenadas para a ROI
    topo_y = h_imagem // 2 - base_h_logo // 2
    esq_x = w_imagem // 2 - base_w_logo // 2
    
    # Define as coordenadas finais, garantindo que não saiam do limite da imagem
    baixo_y = topo_y + base_h_logo
    dir_x = esq_x + base_w_logo

    # Extrai a ROI. A partir daqui, usaremos o tamanho REAL da ROI
    roi = imagem[topo_y:baixo_y, esq_x:dir_x]
    
    # Pega as dimensões reais da ROI extraída
    h_roi, w_roi, _ = roi.shape

    # AQUI ESTÁ A CORREÇÃO PRINCIPAL:
    # Redimensiona o logo para ter o tamanho EXATO da ROI.
    # Isso resolve qualquer problema de arredondamento ou de a ROI estar na borda.
    logo_redimensionado = cv2.resize(logo, (w_roi, h_roi))
    
    # Mistura a ROI com o logo, agora com a garantia de que têm o mesmo tamanho
    resultado = cv2.addWeighted(roi, 1.0 - opacidade, logo_redimensionado, opacidade, 0)

    # Coloca a ROI modificada de volta na imagem principal
    imagem[topo_y:topo_y + h_roi, esq_x:esq_x + w_roi] = resultado
    
    return imagem

def init_config():
    """Cria os diretórios de trabalho se eles não existirem."""
    print("[+] Verificando diretórios...")
    
    if not os.path.exists("imgs_marcadas"):
        os.mkdir("imgs_marcadas")
        print(" -> Diretório 'imgs_marcadas' criado com sucesso.")
    else:
        print(" -> Diretório 'imgs_marcadas' já existe.")

    if not os.path.exists("imgs_nao_marcadas"):
        os.mkdir("imgs_nao_marcadas")
        print(" -> Diretório 'imgs_nao_marcadas' criado com sucesso.")
    else:
        print(" -> Diretório 'imgs_nao_marcadas' já existe.")


def processar_imagens(dir_entrada="imgs_nao_marcadas", dir_saida="imgs_marcadas", logo_path="marca_dagua.png"):
    """
    Processa todas as imagens de um diretório, aplicando a marca d'água.
    """
    print("\n[+] Iniciando processamento de imagens...")

    logo = cv2.imread(logo_path)

    if logo is None:
        print(f"ERRO: Não foi possível carregar o logo em '{logo_path}'. Verifique se o arquivo existe. Abortando.")
        return

    try:
        arquivos = os.listdir(dir_entrada)
    except FileNotFoundError:
        print(f"ERRO: O diretório de entrada '{dir_entrada}' não foi encontrado. Abortando.")
        return

    padrao = re.compile(r'\.(CR2|PNG|JPG|JPEG)$', re.IGNORECASE)
    imagens_a_processar = [f for f in arquivos if padrao.search(f)]
    
    total_imagens = len(imagens_a_processar)
    if total_imagens == 0:
        print(f"[!] Nenhuma imagem encontrada em '{dir_entrada}'.")
        return

    print(f"[+] {total_imagens} imagens encontradas para processar.")

    # Itera sobre cada imagem encontrada
    for i, arquivo in enumerate(imagens_a_processar):
        caminho_completo_entrada = os.path.join(dir_entrada, arquivo)
        print(f" -> Processando ({i + 1}/{total_imagens}): {arquivo}")

        imagem = None
        if arquivo.lower().endswith('.cr2'):
            imagem = ler_img_cr2(caminho_completo_entrada)
        else:
            imagem = cv2.imread(caminho_completo_entrada)

        if imagem is None:
            print(f"    -> Aviso: Não foi possível ler o arquivo {arquivo}. Pulando.")
            continue

        # Aplica a marca d'água na imagem carregada
        imagem_marcada = aplicar_marca_dagua(imagem, logo)
        
        # Cria o nome e o caminho para o arquivo de saída
        nome_base, _ = os.path.splitext(arquivo)
        nome_arquivo_final = f"{nome_base}_marcado.png"
        caminho_final = os.path.join(dir_saida, nome_arquivo_final)
        if imagem_marcada is None:
            continue
        # Salva a imagem processada
        cv2.imwrite(caminho_final, imagem_marcada)
        print(f"    -> Imagem salva em: {caminho_final}")


# --- PONTO DE ENTRADA DO SCRIPT ---

if __name__ == "__main__":
    init_config()

    processar_imagens()
    print("\n[+] Processamento concluído.")

