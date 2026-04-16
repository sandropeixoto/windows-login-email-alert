import os
import socket
import platform
import datetime
import base64
import time
import requests
import resend
import logging
import cv2

# ---------------------------------------------------------------------------
# Configuração — preencha aqui ou defina como variáveis de ambiente
# ---------------------------------------------------------------------------
RESEND_API_KEY = os.getenv("RESEND_API_KEY", "re_SUACHAVE_AQUI")
FROM_EMAIL     = os.getenv("ALERT_FROM", "alerta@seudominio.com")
TO_EMAIL       = os.getenv("ALERT_TO",   "voce@email.com")
# ---------------------------------------------------------------------------

LOG_FILE = os.path.join(os.path.dirname(__file__), "login_alert.log")
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


def get_public_ip() -> str:
    try:
        return requests.get("https://api.ipify.org", timeout=5).text.strip()
    except Exception:
        return "indisponível"


def get_local_ip() -> str:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "indisponível"


def capture_webcam() -> bytes | None:
    """Abre a webcam padrão, aguarda ela estabilizar e captura um frame JPEG."""
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # CAP_DSHOW é mais rápido no Windows
    if not cap.isOpened():
        logging.warning("Webcam não encontrada ou inacessível.")
        return None

    try:
        # Aguarda a câmera estabilizar (exposição automática etc.)
        time.sleep(1.5)
        for _ in range(5):          # descarta frames iniciais escuros
            cap.read()

        ok, frame = cap.read()
        if not ok or frame is None:
            logging.warning("Não foi possível capturar frame da webcam.")
            return None

        _, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        return buf.tobytes()
    finally:
        cap.release()


def build_html(info: dict, has_photo: bool) -> str:
    rows = "".join(
        f"<tr><td style='padding:6px 12px;font-weight:bold;color:#555'>{k}</td>"
        f"<td style='padding:6px 12px'>{v}</td></tr>"
        for k, v in info.items()
    )
    photo_note = (
        "<p>Foto da webcam no momento do login em anexo.</p>"
        if has_photo
        else "<p style='color:#aaa'>Webcam indisponível — nenhuma foto capturada.</p>"
    )
    return f"""
    <html><body style="font-family:sans-serif;color:#222">
    <h2 style="color:#c0392b">Alerta: login detectado no seu computador</h2>
    <table border="0" cellspacing="0" style="border-collapse:collapse;background:#f9f9f9;border-radius:6px">
      {rows}
    </table>
    {photo_note}
    <p style="color:#888;font-size:12px;margin-top:24px">
      Mensagem gerada automaticamente pelo script login_alert.py
    </p>
    </body></html>
    """


def send_alert():
    now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    info = {
        "Data/Hora": now,
        "Computador": socket.gethostname(),
        "Usuário":    os.getlogin(),
        "Sistema":    platform.version(),
        "IP local":   get_local_ip(),
        "IP público": get_public_ip(),
    }

    photo_bytes = capture_webcam()

    resend.api_key = RESEND_API_KEY

    params = {
        "from":    FROM_EMAIL,
        "to":      [TO_EMAIL],
        "subject": f"[Aviso] Login em {info['Computador']} — {now}",
        "html":    build_html(info, has_photo=photo_bytes is not None),
    }

    if photo_bytes:
        params["attachments"] = [
            {
                "filename": "foto_login.jpg",
                "content":  base64.b64encode(photo_bytes).decode(),
            }
        ]

    try:
        response = resend.Emails.send(params)
        logging.info("Email enviado. ID: %s | Info: %s", response.get("id"), info)
    except Exception as e:
        logging.error("Falha ao enviar email: %s | Info: %s", e, info)
        raise


if __name__ == "__main__":
    send_alert()
