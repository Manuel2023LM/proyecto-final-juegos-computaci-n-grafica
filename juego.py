"""Ecos del caos el despertar de los dioses la furia de zeus """

from __future__ import annotations

import math
import random
import subprocess
import sys
import tempfile
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import cv2
import mediapipe as mp
import pygame


# Resolución lógica, escalada al tamaño de la ventana o a pantalla completa.
WIDTH = 960
HEIGHT = 720
FPS = 60
CAMERA_PREVIEW_SIZE = (160, 120)
ROOT = Path(__file__).resolve().parent
PLAYFIELD_LEFT = 34
PLAYFIELD_TOP = 120
PLAYFIELD_RIGHT = WIDTH - 108
PLAYFIELD_BOTTOM = HEIGHT - 30
FORMATION_LEFT_LIMIT = 78
FORMATION_BOTTOM_LIMIT = PLAYFIELD_BOTTOM - 100
PLAYER_MAX_HEALTH = 100
PLAYER_BULLET_DAMAGE = 25
PLAYER_HIT_INVULNERABILITY = 0.7
MIN_WINDOW_SIZE = (800, 600)
VICTORY_INTRO_SECONDS = 10.0
FINAL_VICTORY_MESSAGE = (
    "Venciste al poder del caos. Eres el nuevo dios de la guerra con el poder "
    "del amanecer eterno."
)

# Archivos visuales del proyecto asociados a pantallas y personajes.
ASSET_FILES = {
    "cavern": "Captura de pantalla 2026-11-19 150906.png",
    "portal": "Captura de pantalla 2026-11-19 150914.png",
    "instructions": "Captura de pantalla 2026-11-19 155002.png",
    "menu": "Captura de pantalla 2026-11-19 155025.png",
    "arena": "Captura de pantalla 2026-11-21 192913.png",
    "boss_arena": "Captura de pantalla 2026-11-21 192924.png",
    "frame": "fondo.jpg",
    "player": "sprite-1-1 (2).png",
    "victory": "final.jpg",
}

LEVEL_BACKGROUND_FILES = (
    ("Captura de pantalla 2026-11-21 192913.png", "Captura de pantalla 2026-11-21 192924.png"),
    ("Captura de pantalla 2026-11-21 192934.png", "Captura de pantalla 2026-11-21 193100.png"),
    ("Captura de pantalla 2026-11-21 192511.png", "Captura de pantalla 2026-11-21 192502.png"),
    ("Captura de pantalla 2026-11-21 192739.png", "Captura de pantalla 2026-11-21 192748.png"),
    ("Captura de pantalla 2026-11-21 193002.png", "Captura de pantalla 2026-11-21 193013.png"),
    ("Captura de pantalla 2026-11-21 193107.png", "Captura de pantalla 2026-11-21 193121.png"),
    ("Captura de pantalla 2026-11-21 193131.png", "Captura de pantalla 2026-11-21 193222.png"),
    ("Captura de pantalla 2026-11-21 195932.png", "Captura de pantalla 2026-11-21 195939.png"),
    ("Captura de pantalla 2026-11-21 195952.png", "Captura de pantalla 2026-11-21 195958.png"),
    ("ares_portal.png", "ares_lava_world.png"),
)

LEVEL_ENEMY_SPRITE_FILES = (
    "sprite-1-3 (1).png",
    "sprite-9-1 (1).png",
    "sprite-1-4 (1).png",
    "sprite-1-1 (3).png",
    "sprite-9-2 (1).png",
    "sprite-9-3.png",
    "sprite-1-2 (1).png",
    "sprite-1-5.png",
    "sprite-1-5 (1).png",
    "ares_enemy_blade.png",
)

LEVEL_EXTRA_ENEMY_SPRITE_FILES = {
    10: "ares_enemy_guardian.png",
}

LEVEL_BOSS_SPRITE_FILES = (
    "sprite-1-2 (1).png",
    "sprite-9-1 (2).png",
    "sprite-1-4 (3).png",
    "sprite-9-5 (2).png",
    "sprite-9-2 (2).png",
    "sprite-9-6.png",
    "sprite-1-1.png",
    "sprite-1-1 (10).png",
    "sprite-1-5 (1).png",
    "ares_final_boss.png",
)

LEVEL_NAMES = (
    "Desierto de Helios",
    "Bosque Sombrío",
    "Abismo de Poseidón",
    "Cumbres del Olimpo",
    "Tormenta de Hielo",
    "Portal del Caos",
    "Llamas y Glaciares",
    "Islas Celestiales",
    "Reino Glacial",
    "Mundo de Ares",
)

LEVEL_BOSS_NAMES = (
    "Demonio de las Brasas",
    "Guardián de las Raíces",
    "Kraken de Poseidón",
    "Serafín Dorado",
    "Dragón de la Tormenta",
    "Devorador del Caos",
    "Titán de Fuego",
    "Coloso del Olimpo",
    "Rey del Hielo",
    "Ares, Señor del Caos",
)

LEVEL_STORIES = (
    "Bajo las dunas, Aster encuentra una brújula de bronce. El guardián solar "
    "protegía la primera página de un oráculo que anuncia diez sellos rotos.",
    "Los árboles del bosque repiten una canción olvidada. La semilla que Aster "
    "recupera señala que la amenaza se dirige hacia el mar.",
    "El Kraken custodia una tablilla partida. Sus marcas revelan que los sellos "
    "fueron creados para mantener dormido algo bajo las islas.",
    "En las cumbres, un heraldo reconoce la tablilla y confiesa que su origen "
    "fue ocultado. Una pluma dorada abre el paso a la tormenta.",
    "El dragón de hielo protege el camino del viento. Al vencerlo, Aster descubre "
    "que la tormenta responde a una voz detrás del portal.",
    "El portal muestra los recuerdos de una ciudad evacuada, no otro mundo. "
    "El Devorador custodiaba la ruta hacia antiguas forjas.",
    "En las forjas, el Titán de Fuego despierta el metal de los sellos. Aster "
    "comprende que romperlos liberaría aquello que contienen.",
    "El Coloso intenta cerrar la última ruta sobre las islas. Una estrella "
    "grabada en su armadura señala el reino del hielo.",
    "El Rey del Hielo confiesa que mantenía congelada la grieta. Bajo el reino, "
    "el último titán ya está quebrando la escarcha.",
    "En el mundo de Ares, Aster vence al señor del caos y reclama el amanecer "
    "eterno. La guerra termina, pero el nuevo dios deberá proteger la paz.",
)

LEVEL_PLAYER_AURAS = (
    (255, 171, 75),
    (93, 220, 112),
    (52, 205, 239),
    (255, 222, 125),
    (116, 188, 255),
    (190, 94, 255),
    (255, 105, 68),
    (255, 236, 171),
    (125, 221, 255),
    (255, 104, 35),
)

POWER_IMAGE_FILES = {
    "lightning": "rayo.png",
    "lightning_background": "rayo fondo.png",
    "freeze": "hielo.png",
    "energy": "energia.png",
    "poseidon": "olas de poseidon.png",
    "ares": "fuego.png",
    "ares_flames": "llamas de ares .png",
}

POWER_SOUND_FILES = {
    "lightning": "sonido de rayo.mp4",
    "freeze": "sonido de hielo.mp4",
    "energy": "sonido de energia.mp4",
    "poseidon": "sonido de inundacion.mp4",
    "ares": "sonido de fuego.mp4",
}

EFFECT_SOUND_FILES = {
    "button": "🎌 [EFECTO DE SONIDO] Corte KATANA de Samurai ◾ katana cut samurai sound effect(M4A_128K).m4a.mp4",
    "laser": "lacer.mpeg",
}

INTRO_VIDEO_FILE = "video introduccion.mp4"
LEVEL_FORMATIONS = (
    (2, 4),
    (2, 5),
    (3, 4),
    (3, 5),
    (3, 6),
    (3, 7),
    (4, 6),
    (4, 7),
    (4, 8),
    (5, 8),
)

# Cada nivel tiene su tema y el jefe cambia de música en sus dos fases finales.
MUSIC_FILES = {
    "menu": "sonido1.mp4",
    "level_1": "The Vengeful Spartan (main menu version) - God of War 1 Soundtrack(M4A_128K).m4a.mp4",
    "level_2": "Aegean Storm (First Fight Theme) - God of War 1 Soundtrack(M4A_128K).m4a.mp4",
    "level_3": "Athens Rooftops Fighting (in game version) - God of War 1 Soundtrack(M4A_128K).m4a.mp4",
    "level_4": "Rain of Fire - God of War 1 Soundtrack(M4A_128K).m4a.mp4",
    "level_5": "Poseidon_ Rage - God of War 1 Soundtrack(M4A_128K).m4a.mp4",
    "level_6": "Hall of Atlas (version 1) - God of War 1 Soundtrack(M4A_128K).m4a.mp4",
    "level_7": "sonido6.mp4",
    "level_8": "sonido4.mp4",
    "level_9": "sonido8.mp4",
    "level_10": "sonido7.mp4",
    "boss_phase_1": "sonido3.mp4",
    "boss_phase_1": "sonido3.mp4",
    "boss_phase_2": "sonido2.mp4",
    "boss_phase_3": "sonido5.mp4",
    "victory": "final God of War .m4a.mp4",
}

ZEUS_SOUND = "zeus-le-da-su-poder-a-su-hijo-kratos-furia-de-zeus.mp3"
# Colores comunes de texto y efectos para mantener la paleta del juego.
WHITE = (255, 244, 224)
GOLD = (255, 192, 87)
RED = (255, 89, 61)

ASSET_PATHS = {
    filename: ROOT / directory / filename
    for directory, filenames in {
        Path("assets") / "images" / "backgrounds": (
            {filename for name, filename in ASSET_FILES.items() if name != "player"}
            | {
                filename
                for background_set in LEVEL_BACKGROUND_FILES
                for filename in background_set
            }
        ),
        Path("assets") / "images" / "sprites": (
            {
                ASSET_FILES["player"],
                *LEVEL_ENEMY_SPRITE_FILES,
                *LEVEL_EXTRA_ENEMY_SPRITE_FILES.values(),
                *LEVEL_BOSS_SPRITE_FILES,
            }
        ),
        Path("assets") / "images" / "powers": set(POWER_IMAGE_FILES.values()),
        Path("assets") / "audio" / "music": set(MUSIC_FILES.values()),
        Path("assets") / "audio" / "powers": set(POWER_SOUND_FILES.values()) | {ZEUS_SOUND},
        Path("assets") / "audio" / "effects": set(EFFECT_SOUND_FILES.values()),
        Path("assets") / "video": {INTRO_VIDEO_FILE},
    }.items()
    for filename in filenames
}


@dataclass(frozen=True)
class HandInput:
    """Acciones reconocidas por la cámara durante un ciclo del juego.

    ``move_x`` usa -1, 0 o 1; los campos ``*_pressed`` son eventos puntuales,
    mientras que ``active_powers`` contiene los poderes cuyo gesto sigue activo.
    """

    move_x: int = 0
    shooting: bool = False
    pause_pressed: bool = False
    lightning_pressed: bool = False
    energy_pressed: bool = False
    poseidon_pressed: bool = False
    ares_pressed: bool = False
    freeze_active: bool = False
    active_powers: frozenset[str] = frozenset()


def asset_path(filename: str) -> Path:
    """Devuelve la ruta de un recurso y avisa claramente si no existe."""
    if filename not in ASSET_PATHS:
        raise ValueError(f"Recurso no catalogado: {filename}")
    path = ASSET_PATHS[filename]
    if not path.is_file():
        raise FileNotFoundError(f"No se encontró el recurso del juego: {path}")
    return path


class AudioManager:
    """Convierte y reproduce los temas y efectos de sonido del proyecto."""

    def __init__(self) -> None:
        """Prepara Pygame, FFmpeg y una carpeta temporal para los WAV."""
        try:
            import imageio_ffmpeg
        except ModuleNotFoundError as error:
            raise RuntimeError(
                "Falta imageio-ffmpeg. Instala las dependencias con "
                "'python -m pip install -r requirements.txt'."
            ) from error

        pygame.mixer.init()
        pygame.mixer.set_num_channels(8)
        self.ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
        self.temp_dir = tempfile.TemporaryDirectory(prefix="furia_de_zeus_")
        self.temp_path = Path(self.temp_dir.name)
        self.music_paths: dict[str, Path] = {}
        self.zeus_sound: pygame.mixer.Sound | None = None
        self.power_sounds: dict[str, pygame.mixer.Sound] = {}
        self.power_channels = {
            name: pygame.mixer.Channel(index + 2)
            for index, name in enumerate(POWER_SOUND_FILES)
        }
        self.active_power_sounds: set[str] = set()
        self.effect_sounds: dict[str, pygame.mixer.Sound] = {}
        self.ui_click_channel = pygame.mixer.Channel(7)
        self.shot_channel = pygame.mixer.Channel(0)
        self.shooting_active = False
        self.intro_audio_path: Path | None = None

    def _effect_sound(self, name: str) -> pygame.mixer.Sound:
        """Carga y conserva el efecto de sonido solicitado."""
        if name not in EFFECT_SOUND_FILES:
            raise ValueError(f"Efecto de sonido desconocido: {name}")
        if name not in self.effect_sounds:
            source = asset_path(EFFECT_SOUND_FILES[name])
            destination = self.temp_path / f"{name}_effect.wav"
            self._convert(source, destination)
            sound = pygame.mixer.Sound(str(destination))
            sound.set_volume(0.72 if name == "button" else 0.35)
            self.effect_sounds[name] = sound
        return self.effect_sounds[name]

    def play_ui_click(self) -> None:
        """Reproduce el efecto de espada al activar un botón."""
        self.ui_click_channel.play(self._effect_sound("button"))

    def set_shooting_active(self, active: bool) -> None:
        """Mantiene el láser en bucle solo mientras la nave esté disparando."""
        if active == self.shooting_active:
            return
        if active:
            self.shot_channel.play(self._effect_sound("laser"), loops=-1)
        else:
            self.shot_channel.stop()
        self.shooting_active = active

    def _convert(self, source: Path, destination: Path) -> None:
        """Convierte un audio a WAV mono para que el mezclador de Pygame lo lea."""
        command = [
            self.ffmpeg,
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(source),
            "-vn",
            "-ac",
            "1",
            "-ar",
            "24000",
            "-c:a",
            "pcm_s16le",
            str(destination),
        ]
        try:
            subprocess.run(
                command,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                text=True,
            )
        except subprocess.CalledProcessError as error:
            detail = error.stderr.strip() or "FFmpeg no pudo decodificar el archivo."
            raise RuntimeError(f"No se pudo preparar el audio {source.name}: {detail}") from error

    def _music_path(self, name: str) -> Path:
        """Busca o crea la conversión temporal de un tema musical."""
        if name not in MUSIC_FILES:
            raise ValueError(f"Tema de música desconocido: {name}")
        if name not in self.music_paths:
            source = asset_path(MUSIC_FILES[name])
            destination = self.temp_path / f"{name}.wav"
            self._convert(source, destination)
            self.music_paths[name] = destination
        return self.music_paths[name]

    def play_music(self, name: str) -> None:
        """Reproduce en bucle el tema elegido para la pantalla actual."""
        pygame.mixer.music.stop()
        pygame.mixer.music.load(str(self._music_path(name)))
        pygame.mixer.music.set_volume(0.42)
        pygame.mixer.music.play(-1)

    def play_zeus(self) -> None:
        """Carga una vez y reproduce el efecto de la habilidad de Zeus."""
        if self.zeus_sound is None:
            source = asset_path(ZEUS_SOUND)
            destination = self.temp_path / "furia_de_zeus.wav"
            self._convert(source, destination)
            self.zeus_sound = pygame.mixer.Sound(str(destination))
            self.zeus_sound.set_volume(0.8)
        pygame.mixer.Channel(1).play(self.zeus_sound)

    def play_power(self, name: str) -> None:
        """Reproduce una vez el sonido de un poder."""
        sound = self._power_sound(name)
        self.power_channels[name].play(sound)

    def _power_sound(self, name: str) -> pygame.mixer.Sound:
        """Carga y devuelve el efecto de sonido de un poder."""
        if name not in POWER_SOUND_FILES:
            raise ValueError(f"Efecto de poder desconocido: {name}")
        if name not in self.power_sounds:
            source = asset_path(POWER_SOUND_FILES[name])
            destination = self.temp_path / f"power_{name}.wav"
            self._convert(source, destination)
            sound = pygame.mixer.Sound(str(destination))
            sound.set_volume(0.88)
            self.power_sounds[name] = sound
        return self.power_sounds[name]

    def set_power_active(self, name: str, active: bool) -> None:
        """Mantiene el sonido en bucle mientras el poder siga activo."""
        if name not in POWER_SOUND_FILES:
            raise ValueError(f"Efecto de poder desconocido: {name}")
        if active == (name in self.active_power_sounds):
            return
        channel = self.power_channels[name]
        if active:
            channel.play(self._power_sound(name), loops=-1)
            self.active_power_sounds.add(name)
        else:
            channel.stop()
            self.active_power_sounds.remove(name)
            if name == "lightning":
                pygame.mixer.Channel(1).stop()

    def play_intro_audio(self) -> None:
        """Extrae una vez y reproduce el audio original del video de introduccion."""
        if self.intro_audio_path is None:
            source = asset_path(INTRO_VIDEO_FILE)
            destination = self.temp_path / "intro.wav"
            self._convert(source, destination)
            self.intro_audio_path = destination
        pygame.mixer.music.stop()
        pygame.mixer.music.load(str(self.intro_audio_path))
        pygame.mixer.music.set_volume(0.72)
        pygame.mixer.music.play()

    def close(self) -> None:
        """Detiene el audio y elimina las conversiones temporales."""
        pygame.mixer.music.stop()
        pygame.mixer.stop()
        pygame.mixer.quit()
        self.active_power_sounds.clear()
        self.shooting_active = False
        self.temp_dir.cleanup()


class HandController:
    """Lee la cámara, reconoce gestos y dibuja su vista espejada."""

    # Son las articulaciones y puntas que se resaltan en la vista de cámara.
    gesture_landmark_indices = (4, 6, 8, 10, 12, 14, 16, 18, 20)

    def __init__(self) -> None:
        """Inicia MediaPipe y trata de abrir la cámara predeterminada."""
        self.tracker = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            model_complexity=0,
            min_detection_confidence=0.65,
            min_tracking_confidence=0.6,
        )
        self.capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not self.capture.isOpened():
            self.capture.release()
            self.capture = cv2.VideoCapture(0)
        self.camera_available = self.capture.isOpened()
        if self.camera_available:
            self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.status_text = "CAMARA ACTIVA"
        else:
            self.capture.release()
            self.status_text = "CAMARA NO DISPONIBLE · USA TECLADO"

        self.preview_surface: pygame.Surface | None = None
        self._candidates: dict[str, str | None] = {"Left": None, "Right": None}
        self._stable: dict[str, str | None] = {"Left": None, "Right": None}
        self._candidate_frames: dict[str, int] = {"Left": 0, "Right": 0}
        self._missing_frames: dict[str, int] = {"Left": 0, "Right": 0}
        self.gesture_summary = "MANOS: SIN DETECTAR"

    @staticmethod
    def _gesture_from_fingers(fingers: list[bool]) -> str:
        """Traduce pulgar, índice, medio, anular y meñique a una acción."""
        if len(fingers) == 5:
            if fingers == [True, True, True, True, True]:
                return "open"
            extended = fingers[1:]
        else:
            extended = fingers
        if extended == [True, False, False, False]:
            return "one"
        if extended == [True, True, False, False]:
            return "two"
        if extended == [True, True, True, False]:
            return "three"
        if len(extended) == 4 and extended == [True, True, True, True]:
            return "four"
        if not any(fingers):
            return "fist"
        return "other"

    @staticmethod
    def _fingers_are_spread(landmarks: Any) -> bool:
        """Comprueba que cada punta de dedo esté separada respecto al ancho de palma."""
        palm_width = math.hypot(
            landmarks[5].x - landmarks[17].x,
            landmarks[5].y - landmarks[17].y,
        )
        if palm_width <= 1e-6:
            return False
        tips = (4, 8, 12, 16, 20)
        minimum_gap = palm_width * 0.18
        return all(
            math.hypot(
                landmarks[left].x - landmarks[right].x,
                landmarks[left].y - landmarks[right].y,
            )
            >= minimum_gap
            for left, right in zip(tips, tips[1:])
        )

    @classmethod
    def _classify_landmarks(cls, landmarks: Any, side: str) -> str:
        """Determina los cinco dedos y compensa la camara reflejada."""
        # MediaPipe: 8/12/16/20 son puntas; 6/10/14/18 son sus articulaciones.
        tips = (8, 12, 16, 20)
        joints = (6, 10, 14, 18)
        fingers = [
            landmarks[4].x > landmarks[3].x
            if side == "Right"
            else landmarks[4].x < landmarks[3].x
        ]
        fingers.extend(
            landmarks[tip].y < landmarks[joint].y
            for tip, joint in zip(tips, joints)
        )
        gesture = cls._gesture_from_fingers(fingers)
        if gesture == "open" and not cls._fingers_are_spread(landmarks):
            return "other"
        return gesture

    def _stabilize(self, side: str, gesture: str) -> tuple[str | None, bool]:
        """Exige tres cuadros iguales para evitar acciones por detecciones fugaces."""
        if gesture == self._candidates[side]:
            self._candidate_frames[side] += 1
        else:
            self._candidates[side] = gesture
            self._candidate_frames[side] = 1

        if self._candidate_frames[side] >= 3 and self._stable[side] != gesture:
            self._stable[side] = gesture
            return gesture, True
        return self._stable[side], False

    def _forget(self, side: str) -> None:
        """Borra el gesto anterior cuando la mano deja de aparecer en cámara."""
        self._candidates[side] = None
        self._candidate_frames[side] = 0
        self._missing_frames[side] = 0
        self._stable[side] = None

    def poll(self) -> HandInput:
        """Lee un cuadro espejado, marca puntos y devuelve las acciones detectadas."""
        if not self.camera_available:
            return HandInput()

        success, frame = self.capture.read()
        if not success:
            self.camera_available = False
            self.capture.release()
            self.status_text = "CAMARA DESCONECTADA · USA TECLADO"
            self.gesture_summary = "MANOS: SIN DETECTAR"
            self._forget("Left")
            self._forget("Right")
            return HandInput()

        # Se refleja antes de analizar y mostrar para que la vista coincida con el movimiento.
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.tracker.process(rgb_frame)
        annotated_frame = frame.copy()
        if result.multi_hand_landmarks:
            frame_height, frame_width = annotated_frame.shape[:2]
            for hand in result.multi_hand_landmarks:
                points = [
                    (round(point.x * frame_width), round(point.y * frame_height))
                    for point in hand.landmark
                ]
                for start, end in mp.solutions.hands.HAND_CONNECTIONS:
                    cv2.line(
                        annotated_frame,
                        points[start],
                        points[end],
                        (70, 105, 235),
                        2,
                        cv2.LINE_AA,
                    )
                for index, point in enumerate(points):
                    # Amarillo identifica las articulaciones usadas por el clasificador.
                    radius = 8 if index in self.gesture_landmark_indices else 4
                    color = (0, 255, 255) if index in self.gesture_landmark_indices else (70, 190, 255)
                    cv2.circle(annotated_frame, point, radius, color, -1, cv2.LINE_AA)

        preview = cv2.resize(
            annotated_frame, CAMERA_PREVIEW_SIZE, interpolation=cv2.INTER_AREA
        )
        preview = cv2.cvtColor(preview, cv2.COLOR_BGR2RGB)
        self.preview_surface = pygame.image.frombuffer(
            preview.tobytes(), CAMERA_PREVIEW_SIZE, "RGB"
        ).copy()
        gestures: dict[str, str | None] = {"Left": None, "Right": None}
        changed: dict[str, bool] = {"Left": False, "Right": False}
        detected: set[str] = set()

        if result.multi_hand_landmarks and result.multi_handedness:
            for hand, handedness in zip(result.multi_hand_landmarks, result.multi_handedness):
                side = handedness.classification[0].label
                detected.add(side)
                gestures[side], changed[side] = self._stabilize(
                    side, self._classify_landmarks(hand.landmark, side)
                )

        for side in ("Left", "Right"):
            if side not in detected:
                # Se toleran unos cuadros perdidos para evitar que el gesto parpadee.
                self._missing_frames[side] += 1
                if self._missing_frames[side] >= 6:
                    self._forget(side)
                gestures[side] = self._stable[side]
            else:
                self._missing_frames[side] = 0

        right = gestures["Right"]
        left = gestures["Left"]
        right_names = {
            "one": "IZQ",
            "two": "DER",
            "three": "PAUSA",
            "fist": "DISPARO",
        }
        left_names = {
            "one": "RAYO",
            "two": "HIELO",
            "three": "ENERGIA",
            "four": "POSEIDON",
            "open": "ARES",
        }
        right_label = right_names.get(right, "—")
        left_label = left_names.get(left, "—")
        if not detected:
            self.status_text = "CAMARA ACTIVA · MUESTRA LAS MANOS"
            self.gesture_summary = "MANOS: BUSCANDO"
        else:
            self.status_text = "CAMARA ACTIVA"
            self.gesture_summary = f"DER: {right_label}  |  IZQ: {left_label}"

        # Los poderes se activan al entrar en el gesto y se muestran mientras se sostiene.
        left_power = {
            "one": "lightning",
            "two": "freeze",
            "three": "energy",
            "four": "poseidon",
            "open": "ares",
        }.get(left)
        return HandInput(
            move_x=-1 if right == "one" else 1 if right == "two" else 0,
            shooting=right == "fist",
            pause_pressed=right == "three" and changed["Right"],
            lightning_pressed=left == "one" and changed["Left"],
            energy_pressed=left == "three" and changed["Left"],
            poseidon_pressed=left == "four" and changed["Left"],
            ares_pressed=left == "open" and changed["Left"],
            freeze_active=left == "two",
            active_powers=frozenset((left_power,)) if left_power else frozenset(),
        )

    def close(self) -> None:
        """Libera la cámara y el modelo de seguimiento de manos."""
        self.capture.release()
        self.tracker.close()


class Game:
    """Coordina las pantallas, reglas, controles y presentación del juego."""

    keyboard_power_keys = {
        pygame.K_e: "lightning",
        pygame.K_1: "lightning",
        pygame.K_2: "freeze",
        pygame.K_3: "energy",
        pygame.K_4: "poseidon",
        pygame.K_5: "ares",
    }

    def __init__(self, use_camera: bool = True) -> None:
        """Crea la ventana, carga recursos y prepara el estado inicial del menú."""
        pygame.init()
        pygame.display.set_caption("Furia de Zeus: Ecos del Caos")
        self.windowed_size = (WIDTH, HEIGHT)
        self.display = pygame.display.set_mode(self.windowed_size, pygame.RESIZABLE)
        self.screen = pygame.Surface((WIDTH, HEIGHT))
        self.viewport = pygame.Rect(0, 0, WIDTH, HEIGHT)
        self.fullscreen = False
        self.clock = pygame.time.Clock()
        self.audio = AudioManager()
        self.hand_controller = HandController() if use_camera else None
        self.font = pygame.font.SysFont("arial", 24, bold=True)
        self.small_font = pygame.font.SysFont("arial", 18, bold=True)
        self.title_font = pygame.font.SysFont("georgia", 48, bold=True)
        self.story_kicker_font = pygame.font.SysFont("georgia", 22, bold=True)
        self.story_title_font = pygame.font.SysFont("georgia", 42, bold=True)
        self.story_body_font = pygame.font.SysFont("georgia", 26, italic=True)
        self._text_surface_cache: dict[
            tuple[int, str, tuple[int, int, int]],
            tuple[pygame.Surface, pygame.Surface],
        ] = {}
        self._panel_surface_cache: dict[
            tuple[tuple[int, int], tuple[int, int, int, int]],
            pygame.Surface,
        ] = {}
        self.arena_shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.arena_shade.fill((8, 5, 14, 105))
        self.low_life_filter = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.low_life_filter.fill((180, 0, 20, 48))
        self.images = self._load_images()
        self.victory_image = self._fit_image(self.images["victory"], (WIDTH, HEIGHT))
        self.backgrounds = {
            "menu": self._cover(self.images["menu"]),
            "instructions": self._cover(self.images["instructions"]),
            "cavern": self._cover(self.images["cavern"]),
            "portal": self._cover(self.images["portal"]),
        }
        self.level_backgrounds = [
            tuple(
                self._prepare_level_background(
                    self.images[f"level_{level}_background_{phase}"]
                )
                for phase in range(len(background_files))
            )
            for level, background_files in enumerate(LEVEL_BACKGROUND_FILES, start=1)
        ]
        self.level_previews = [
            self._fit_image(backgrounds[0], (144, 100))
            for backgrounds in self.level_backgrounds
        ]
        self.enemy_images = [
            self._prepare_sprite(self.images[f"enemy_{level}"], (58, 68))
            for level in range(1, len(LEVEL_ENEMY_SPRITE_FILES) + 1)
        ]
        self.extra_enemy_images = {
            level: self._prepare_sprite(self.images[f"enemy_extra_{level}"], (58, 68))
            for level in LEVEL_EXTRA_ENEMY_SPRITE_FILES
        }
        self.boss_images = [
            self._prepare_sprite(self.images[f"boss_{level}"], (270, 240))
            for level in range(1, len(LEVEL_BOSS_SPRITE_FILES) + 1)
        ]
        self.player_image = self._prepare_sprite(self.images["player"], (62, 78))
        self.boss_image = self.boss_images[0]
        self.player_aura = LEVEL_PLAYER_AURAS[0]
        self.power_images = {
            name: self.images[f"power_{name}"]
            for name in POWER_IMAGE_FILES
        }
        self.power_icons = {
            name: self._fit_image(self.power_images[name], (52, 52))
            for name in ("lightning", "freeze", "energy", "poseidon", "ares")
        }
        self.lightning_icon_backdrop = pygame.transform.smoothscale(
            self.power_images["lightning_background"], (54, 54)
        )
        self.power_effect_images = {
            "lightning": self._fit_image(self.power_images["lightning"], (280, 240)),
            "lightning_aura": self._fit_image(
                self.power_images["lightning_background"],
                (260, 222),
            ),
            "freeze": self._fit_image(self.power_images["freeze"], (280, 240)),
            "energy": self._fit_image(self.power_images["energy"], (280, 240)),
            "poseidon": self._fit_image(self.power_images["poseidon"], (280, 240)),
            "ares": self._fit_image(self.power_images["ares_flames"], (280, 240)),
        }
        self.lightning_aura_effect = self.power_effect_images["lightning_aura"].copy()
        self.lightning_aura_effect.set_alpha(120)
        self._wallpaper_cache: pygame.Surface | None = None
        self._wallpaper_cache_size: tuple[int, int] | None = None
        self.state = "menu"
        self.selected_level = 1
        self.intro_frames: Any | None = None
        self.intro_frame_size = (0, 0)
        self.intro_fps = 30.0
        self.intro_accumulator = 0.0
        self.intro_frame_surface: pygame.Surface | None = None
        self.boss_intro_timer = 0.0
        self.victory_intro_timer = 0.0
        self.story_text = ""
        self.story_revealed_chars = 0
        self.story_reveal_progress = 0.0
        self.show_camera_preview = True
        self.score = 0
        self.best_score = 0
        self.level = 1
        self.level_boss_name = LEVEL_BOSS_NAMES[0]
        self.lives = 3
        self.player_health = PLAYER_MAX_HEALTH
        self.special_charges = 3
        self.power_cooldowns = {
            "energy": 0.0,
            "poseidon": 0.0,
            "ares": 0.0,
        }
        self.active_powers: set[str] = set()
        self.keyboard_power_keys_down: set[int] = set()
        self.keyboard_freeze = False
        self.is_frozen = False
        self.enemies: list[dict[str, Any]] = []
        self.bullets: list[dict[str, Any]] = []
        self.ray_effects: list[dict[str, Any]] = []
        self.boss: dict[str, Any] | None = None
        self.player = pygame.Rect(WIDTH // 2 - 31, HEIGHT - 104, 62, 78)
        self.player_cooldown = 0.0
        self.enemy_fire_timer = 0.8
        self.invulnerability = 0.0
        self.formation_direction = 1
        self.formation_vertical_direction = 1
        self.formation_speed = 52.0
        self.stage_enemy_count = 0
        self.wave_index = 0
        self.wave_sizes: tuple[int, ...] = (0, 0, 0)
        self.tiny_font = pygame.font.SysFont("arial", 14, bold=True)
        self.menu_buttons = [
            (pygame.Rect(350, 241, 260, 52), "JUGAR"),
            (pygame.Rect(350, 307, 260, 52), "ELEGIR NIVEL"),
            (pygame.Rect(350, 373, 260, 52), "INSTRUCCIONES"),
            (pygame.Rect(350, 439, 260, 52), "PUNTAJE"),
            (pygame.Rect(350, 505, 260, 52), "SALIR"),
        ]
        self.level_buttons = [
            pygame.Rect(95 + index % 5 * 153, 255 + index // 5 * 166, 146, 156)
            for index in range(10)
        ]
        self.next_level_button = pygame.Rect(350, 592, 260, 42)
        self.victory_menu_button = pygame.Rect(350, 652, 260, 42)
        self.fullscreen_toggle_button = pygame.Rect(320, 644, 320, 44)
        self.pause_resume_button = pygame.Rect(350, 382, 260, 58)
        self.audio.play_music("menu")

    def _load_images(self) -> dict[str, pygame.Surface]:
        """Carga fondos y sprites; informa claramente si algún recurso no existe."""
        images: dict[str, pygame.Surface] = {}
        files = dict(ASSET_FILES)
        files.update(
            {
                f"enemy_{level}": filename
                for level, filename in enumerate(LEVEL_ENEMY_SPRITE_FILES, start=1)
            }
        )
        files.update(
            {
                f"enemy_extra_{level}": filename
                for level, filename in LEVEL_EXTRA_ENEMY_SPRITE_FILES.items()
            }
        )
        files.update(
            {
                f"boss_{level}": filename
                for level, filename in enumerate(LEVEL_BOSS_SPRITE_FILES, start=1)
            }
        )
        files.update(
            {
                f"power_{name}": filename
                for name, filename in POWER_IMAGE_FILES.items()
            }
        )
        for level, background_files in enumerate(LEVEL_BACKGROUND_FILES, start=1):
            files.update(
                {
                    f"level_{level}_background_{phase}": filename
                    for phase, filename in enumerate(background_files)
                }
            )

        for name, filename in files.items():
            try:
                path = asset_path(filename)
                loaded = pygame.image.load(str(path))
                keep_alpha = (
                    name == "player"
                    or name.startswith(("enemy_", "boss_", "power_"))
                )
                images[name] = loaded.convert_alpha() if keep_alpha else loaded.convert()
            except (FileNotFoundError, pygame.error) as error:
                warnings.warn(
                    f"No se pudo cargar {filename}; se usará una imagen de respaldo: {error}",
                    RuntimeWarning,
                    stacklevel=2,
                )
                images[name] = self._fallback_image(name)
        return images

    @staticmethod
    def _fallback_image(name: str) -> pygame.Surface:
        """Crea una imagen sustituta para que un recurso faltante sea visible."""
        is_sprite = name == "player" or name.startswith(("enemy_", "boss_", "power_"))
        size = (128, 128) if is_sprite else (WIDTH, HEIGHT)
        image = pygame.Surface(size, pygame.SRCALPHA if is_sprite else 0)
        image.fill((0, 0, 0, 0) if is_sprite else (3, 0, 8))
        width, height = size
        if is_sprite:
            pygame.draw.polygon(
                image,
                (180, 22, 42),
                [
                    (width // 2, height // 8),
                    (width - 8, height // 2),
                    (width // 2, height * 7 // 8),
                    (8, height // 2),
                ],
            )
            pygame.draw.circle(
                image, (255, 175, 75), (width // 2, height // 2), 10
            )
            return image

        for y in range(0, height, 48):
            pygame.draw.line(image, (28, 0, 12), (0, y), (width, y), 1)
        for x in range(0, width, 64):
            pygame.draw.line(image, (22, 0, 10), (x, 0), (x, height), 1)
        pygame.draw.ellipse(
            image,
            (100, 8, 24),
            (width // 4, height // 4, width // 2, height // 2),
            max(1, width // 120),
        )
        pygame.draw.line(
            image,
            (120, 10, 28),
            (0, height),
            (width, 0),
            max(2, width // 240),
        )
        label = pygame.font.Font(None, 30).render(
            "IMAGEN AUSENTE", True, (235, 70, 82)
        )
        image.blit(label, label.get_rect(center=(width // 2, height - 38)))
        return image

    @staticmethod
    def _cover(image: pygame.Surface) -> pygame.Surface:
        """Escala y recorta una imagen para cubrir la resolución lógica completa."""
        scale = max(WIDTH / image.get_width(), HEIGHT / image.get_height())
        size = (round(image.get_width() * scale), round(image.get_height() * scale))
        scaled = pygame.transform.smoothscale(image, size)
        result = pygame.Surface((WIDTH, HEIGHT))
        result.blit(
            scaled,
            ((WIDTH - size[0]) // 2, (HEIGHT - size[1]) // 2),
        )
        return result

    @classmethod
    def _prepare_level_background(cls, image: pygame.Surface) -> pygame.Surface:
        """Prepara una escena centrada para evitar reescalar imágenes cada cuadro."""
        result = cls._cover(image)
        scale = min(620 / image.get_width(), 660 / image.get_height())
        size = (
            round(image.get_width() * scale),
            round(image.get_height() * scale),
        )
        centered_image = pygame.transform.smoothscale(image, size)
        result.blit(
            centered_image,
            centered_image.get_rect(center=(WIDTH // 2, HEIGHT // 2)),
        )
        return result

    @staticmethod
    def _prepare_sprite(
        image: pygame.Surface, size: tuple[int, int]
    ) -> pygame.Surface:
        """Escala un sprite sin quitar su transparencia original."""
        return Game._fit_image(image, size)

    @staticmethod
    def _fit_image(image: pygame.Surface, size: tuple[int, int]) -> pygame.Surface:
        """Ajusta una imagen dentro de un rectangulo sin deformar su proporcion."""
        scale = min(size[0] / image.get_width(), size[1] / image.get_height())
        fitted_size = (
            max(1, round(image.get_width() * scale)),
            max(1, round(image.get_height() * scale)),
        )
        fitted = pygame.transform.smoothscale(image.convert_alpha(), fitted_size)
        result = pygame.Surface(size, pygame.SRCALPHA)
        result.blit(fitted, fitted.get_rect(center=(size[0] // 2, size[1] // 2)))
        return result

    def _draw_text(
        self,
        text: str,
        center: tuple[int, int],
        color: tuple[int, int, int] = WHITE,
        font: pygame.font.Font | None = None,
    ) -> None:
        """Dibuja texto con sombra para que contraste con los fondos oscuros."""
        selected_font = font or self.font
        cache_key = (id(selected_font), text, color)
        cached_surfaces = self._text_surface_cache.get(cache_key)
        if cached_surfaces is None:
            label = selected_font.render(text, True, color)
            shadow = selected_font.render(text, True, (32, 12, 12))
            if len(self._text_surface_cache) >= 512:
                self._text_surface_cache.pop(next(iter(self._text_surface_cache)))
            self._text_surface_cache[cache_key] = (label, shadow)
        else:
            label, shadow = cached_surfaces
        shadow_rect = shadow.get_rect(center=(center[0] + 2, center[1] + 3))
        label_rect = label.get_rect(center=center)
        self.screen.blit(shadow, shadow_rect)
        self.screen.blit(label, label_rect)

    def _panel(self, rect: pygame.Rect, color: tuple[int, int, int, int]) -> None:
        """Pinta un panel translúcido sin alterar el fondo que hay debajo."""
        cache_key = (rect.size, color)
        surface = self._panel_surface_cache.get(cache_key)
        if surface is None:
            surface = pygame.Surface(rect.size, pygame.SRCALPHA)
            surface.fill(color)
            if len(self._panel_surface_cache) >= 128:
                self._panel_surface_cache.pop(next(iter(self._panel_surface_cache)))
            self._panel_surface_cache[cache_key] = surface
        self.screen.blit(surface, rect.topleft)

    def _logical_mouse_position(self) -> tuple[int, int]:
        """Convierte el cursor de la ventana al espacio de coordenadas del juego."""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return (
            round((mouse_x - self.viewport.x) * WIDTH / self.viewport.width),
            round((mouse_y - self.viewport.y) * HEIGHT / self.viewport.height),
        )

    def _draw_menu(self) -> None:
        """Muestra el menú principal y el botón para cambiar a pantalla completa."""
        self.screen.blit(self.backgrounds["menu"], (0, 0))
        self._panel(pygame.Rect(314, 224, 332, 346), (19, 10, 13, 238))
        pygame.draw.rect(self.screen, (153, 64, 43), (314, 224, 332, 346), 3)
        self._draw_text("FURIA DE ZEUS", (WIDTH // 2, 167), GOLD, self.title_font)
        for rect, label in self.menu_buttons:
            hovered = rect.collidepoint(self._logical_mouse_position())
            fill = (104, 35, 29, 240) if hovered else (59, 27, 24, 230)
            self._panel(rect, fill)
            pygame.draw.rect(self.screen, GOLD if hovered else (183, 103, 55), rect, 2)
            self._draw_text(label, rect.center, WHITE, self.small_font)
        self._draw_text(
            "JUGAR reproduce la introduccion · ENTER permite saltarla",
            (480, 598),
            GOLD,
            self.small_font,
        )
        camera_status = (
            self.hand_controller.status_text
            if self.hand_controller is not None
            else "CONTROLES DE TECLADO"
        )
        self._draw_text(camera_status, (480, 630), WHITE, self.small_font)
        hovered = self.fullscreen_toggle_button.collidepoint(
            self._logical_mouse_position()
        )
        self._panel(
            self.fullscreen_toggle_button,
            (104, 22, 31, 240) if hovered else (45, 10, 18, 230),
        )
        pygame.draw.rect(
            self.screen,
            GOLD if hovered else (183, 103, 55),
            self.fullscreen_toggle_button,
            2,
        )
        mode = "SI" if self.fullscreen else "NO"
        self._draw_text(
            f"PANTALLA COMPLETA: {mode} · F11",
            self.fullscreen_toggle_button.center,
            WHITE,
            self.small_font,
        )
        self._draw_text("V: VISTA DE CAMARA", (480, 700), GOLD, self.small_font)

    def _draw_level_select(self) -> None:
        """Presenta los diez mundos y permite escoger cualquiera."""
        self.screen.blit(self.backgrounds["menu"], (0, 0))
        panel = pygame.Rect(76, 202, 808, 392)
        self._panel(panel, (12, 8, 15, 235))
        pygame.draw.rect(self.screen, (153, 64, 43), panel, 3)
        self._draw_text("ELIGE TU MUNDO", (WIDTH // 2, 222), GOLD, self.title_font)
        for index, rect in enumerate(self.level_buttons):
            hovered = rect.collidepoint(self._logical_mouse_position())
            selected = index + 1 == self.selected_level
            self._panel(rect, (18, 12, 16, 245))
            preview_rect = pygame.Rect(rect.x + 1, rect.y + 1, rect.width - 2, 101)
            self.screen.blit(self.level_previews[index], preview_rect)
            self._panel(preview_rect, (4, 3, 10, 62))
            border = GOLD if hovered or selected else (126, 74, 51)
            pygame.draw.rect(self.screen, border, rect, 2)
            self._draw_text(
                f"NIVEL {index + 1}",
                (rect.centerx, rect.y + 113),
                GOLD,
                self.small_font,
            )
            self._draw_text(
                LEVEL_NAMES[index],
                (rect.centerx, rect.y + 139),
                WHITE,
                self.tiny_font,
            )
        self._draw_text(
            "Haz clic en un mundo · teclas 1-9 o 0 · ESC para volver",
            (WIDTH // 2, 620),
            GOLD,
            self.small_font,
        )

    def _draw_intro(self) -> None:
        """Muestra el video de apertura y la indicacion para saltarlo."""
        self.screen.blit(self.backgrounds["menu"], (0, 0))
        if self.intro_frame_surface is not None:
            frame_width, frame_height = self.intro_frame_surface.get_size()
            scale = min(WIDTH / frame_width, HEIGHT / frame_height)
            size = (
                round(frame_width * scale),
                round(frame_height * scale),
            )
            frame = pygame.transform.smoothscale(self.intro_frame_surface, size)
            self.screen.blit(frame, frame.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        hint = pygame.Rect(WIDTH - 350, HEIGHT - 58, 334, 40)
        self._panel(hint, (12, 7, 10, 225))
        pygame.draw.rect(self.screen, GOLD, hint, 1)
        self._draw_text(
            "ENTER: SALTAR INTRO",
            hint.center,
            WHITE,
            self.small_font,
        )

    def _draw_instructions(self) -> None:
        """Explica los gestos de ambas manos y los controles alternativos."""
        self.screen.blit(self.backgrounds["instructions"], (0, 0))
        self._panel(pygame.Rect(115, 42, 730, 636), (15, 11, 17, 226))
        self._draw_text("CONTROLES CON LAS MANOS", (WIDTH // 2, 93), GOLD, self.title_font)
        instructions = [
            ("MOVER", "Mano derecha: indice = izquierda; indice + medio = derecha"),
            ("DISPARAR", "Mano derecha: puño cerrado; teclado: Espacio"),
            ("PAUSA", "Mano derecha: tres dedos; teclado: Esc"),
            ("RAYO", "Mano izquierda: solo indice"),
            ("CONGELAR", "Mano izquierda: indice + medio"),
            ("ENERGIA", "Mano izquierda: indice + medio + anular"),
            ("OLAS DE POSEIDON", "Mano izquierda: indice + medio + anular + meñique"),
            ("FUEGO DE ARES", "Mano izquierda: cinco dedos levantados y separados"),
            ("TECLADO", "Flechas/WASD, espacio, E y 1-5 para poderes; Esc pausa"),
            ("NIVELES", "JUGAR reproduce la intro; ELEGIR NIVEL abre los diez mundos"),
        ]
        for index, (heading, detail) in enumerate(instructions):
            y = 151 + index * 43
            self._draw_text(heading, (WIDTH // 2 - 245, y), GOLD, self.tiny_font)
            self._draw_text(detail, (WIDTH // 2 + 105, y), WHITE, self.tiny_font)
        self._draw_text(
            "Suelta el gesto para detener la imagen y el sonido; la tecla 2 alterna el hielo.",
            (WIDTH // 2, 585),
            WHITE,
            self.tiny_font,
        )
        self._draw_text("Haz clic o presiona ENTER para volver", (WIDTH // 2, 625), GOLD, self.small_font)

    def _draw_arena_background(self) -> None:
        """Centra el arte completo del nivel sobre su fondo ampliado y oscurecido."""
        backgrounds = self.level_backgrounds[self.level - 1]
        phase = int(
            len(backgrounds) > 1
            and self.stage_enemy_count > 0
            and len(self.enemies) <= self.stage_enemy_count // 2
        )
        self.screen.blit(backgrounds[phase], (0, 0))
        self.screen.blit(self.arena_shade, (0, 0))

    def _draw_game(self) -> None:
        """Dibuja escenario, proyectiles, enemigos, jefe y HUD de la partida."""
        self._draw_arena_background()
        for bullet in self.bullets:
            pygame.draw.rect(self.screen, bullet["color"], bullet["rect"], border_radius=4)
            pygame.draw.circle(
                self.screen,
                (255, 237, 175),
                bullet["rect"].center,
                max(2, bullet["rect"].width // 2),
            )

        for enemy in self.enemies:
            enemy_image = self.enemy_images[self.level - 1]
            if enemy.get("variant"):
                enemy_image = self.extra_enemy_images.get(self.level, enemy_image)
            self.screen.blit(
                enemy_image, enemy_image.get_rect(center=enemy["rect"].center)
            )
            if self.is_frozen:
                pygame.draw.ellipse(
                    self.screen,
                    (93, 218, 255),
                    enemy["rect"].inflate(8, 8),
                    2,
                )

        if self.boss is not None:
            boss_rect = self.boss["rect"]
            self.screen.blit(self.boss_image, self.boss_image.get_rect(center=boss_rect.center))
            pygame.draw.ellipse(self.screen, (190, 25, 30), boss_rect.inflate(34, 30), 5)
            if self.is_frozen or self.boss["stun_timer"] > 0:
                pygame.draw.ellipse(
                    self.screen,
                    (93, 218, 255),
                    boss_rect.inflate(48, 42),
                    5,
                )
            self._draw_boss_health()

        self._draw_ray_effects()
        self._draw_power_effects()
        if self.invulnerability <= 0 or int(self.invulnerability * 12) % 2 == 0:
            pygame.draw.ellipse(
                self.screen,
                self.player_aura,
                self.player.inflate(18, 12),
                2,
            )
            self.screen.blit(
                self.player_image,
                self.player_image.get_rect(center=self.player.center),
            )

        self._draw_hud()
        if self.lives == 1 and self.player_health <= 25:
            self.screen.blit(self.low_life_filter, (0, 0))

    def _draw_ray_effects(self) -> None:
        """Traza rayos dentados desde la nave hasta cada objetivo del ataque."""
        for effect in self.ray_effects:
            for points in effect["rays"]:
                pygame.draw.lines(self.screen, (115, 10, 24), False, points, 8)
                pygame.draw.lines(self.screen, (255, 65, 34), False, points, 4)
                pygame.draw.lines(self.screen, (255, 230, 150), False, points, 1)

    def _draw_power_effects(self) -> None:
        """Muestra las ilustraciones de los poderes mientras su entrada siga activa."""
        if self.active_powers:
            self.screen.blit(
                self.lightning_aura_effect,
                self.lightning_aura_effect.get_rect(
                    center=(WIDTH // 2, HEIGHT // 2)
                ),
            )
        active_names = [
            power for power in POWER_SOUND_FILES if power in self.active_powers
        ]
        for index, name in enumerate(active_names):
            image = self.power_effect_images[name]
            spacing = min(
                220,
                (WIDTH - image.get_width()) / max(1, len(active_names) - 1),
            )
            center = (
                round(
                    WIDTH // 2
                    + (index - (len(active_names) - 1) / 2) * spacing
                ),
                HEIGHT // 2,
            )
            self.screen.blit(image, image.get_rect(center=center))
            if name == "poseidon":
                pygame.draw.circle(
                    self.screen,
                    (67, 196, 255),
                    center,
                    min(image.get_size()) // 2,
                    3,
                )

    def _draw_boss_health(self) -> None:
        """Muestra la barra de vida del jefe sobre su retrato."""
        bar = pygame.Rect(365, 75, 360, 20)
        pygame.draw.rect(self.screen, (35, 13, 16), bar)
        if self.boss is not None:
            health = max(0, self.boss["health"])
            fill = pygame.Rect(
                bar.x,
                bar.y,
                round(bar.width * health / self.boss["max_health"]),
                bar.height,
            )
            pygame.draw.rect(self.screen, RED, fill)
        pygame.draw.rect(self.screen, WHITE, bar, 2)
        self._draw_text(self.level_boss_name, (545, 54), GOLD, self.small_font)

    def _draw_hud(self) -> None:
        """Muestra estado del mundo y los cinco poderes con sus iconos."""
        self._panel(pygame.Rect(14, 14, 340, 90), (15, 10, 13, 220))
        self._draw_text(
            LEVEL_NAMES[self.level - 1],
            (WIDTH // 2, 34),
            GOLD,
            self.small_font,
        )
        self._draw_text(
            f"NIVEL {self.level}/10",
            (248, 30),
            GOLD,
            self.tiny_font,
        )
        self._draw_text(
            f"OLEADA {self.wave_index + 1}/{len(self.wave_sizes)}",
            (248, 52),
            GOLD,
            self.tiny_font,
        )
        self._draw_text(
            f"VIDAS {self.lives}  PTS {self.score:06d}",
            (248, 78),
            GOLD,
            self.tiny_font,
        )
        self._draw_player_health()
        self._draw_text("PODERES", (WIDTH - 50, 180), GOLD, self.tiny_font)
        labels = ("RAYO", "HIELO", "ENERGIA", "POSEIDON", "ARES")
        power_names = ("lightning", "freeze", "energy", "poseidon", "ares")
        for index, (name, label) in enumerate(zip(power_names, labels)):
            tile = pygame.Rect(WIDTH - 86, 198 + index * 88, 72, 76)
            self._panel(tile, (12, 8, 14, 218))
            if name in self.active_powers:
                pygame.draw.rect(self.screen, GOLD, tile.inflate(4, 4), 2)
            if name == "lightning":
                self.screen.blit(
                    self.lightning_icon_backdrop,
                    self.lightning_icon_backdrop.get_rect(
                        center=(tile.centerx, tile.y + 25)
                    ),
                )
            icon = self.power_icons[name]
            self.screen.blit(icon, icon.get_rect(center=(tile.centerx, tile.y + 25)))
            displayed_label = f"RAYO {self.special_charges}" if name == "lightning" else label
            self._draw_text(
                displayed_label,
                (tile.centerx, tile.y + 63),
                GOLD
                if name in self.active_powers
                or (name == "lightning" and self.special_charges > 0)
                or self.power_cooldowns.get(name, 0) <= 0
                else (145, 145, 145),
                self.tiny_font,
            )
        if self.hand_controller is not None:
            self._draw_text(
                self.hand_controller.gesture_summary,
                (WIDTH - 238, 178),
                WHITE,
                self.tiny_font,
            )

    def _draw_player_health(self) -> None:
        """Dibuja la salud dentro de la esquina superior izquierda del HUD."""
        ratio = max(0.0, min(1.0, self.player_health / PLAYER_MAX_HEALTH))
        bar = pygame.Rect(24, 48, 108, 13)
        pygame.draw.rect(self.screen, (16, 11, 15), bar, border_radius=4)
        fill_color = (
            (72, 220, 125)
            if ratio > 0.6
            else GOLD
            if ratio > 0.3
            else (255, 82, 72)
        )
        fill = pygame.Rect(
            bar.x + 1,
            bar.y + 1,
            round((bar.width - 2) * ratio),
            bar.height - 2,
        )
        if fill.width > 0:
            pygame.draw.rect(self.screen, fill_color, fill, border_radius=3)
        pygame.draw.rect(self.screen, WHITE, bar, 1, border_radius=4)
        self._draw_text(
            f"SALUD {self.player_health}%",
            (78, 80),
            GOLD,
            self.tiny_font,
        )

    def _draw_camera_preview(self) -> None:
        """Coloca la vista espejo con puntos en una esquina del juego."""
        if self.hand_controller is None or not self.show_camera_preview:
            return

        panel = pygame.Rect(WIDTH - 178, 12, 168, 150)
        self._panel(panel, (12, 8, 12, 225))
        preview = self.hand_controller.preview_surface
        if preview is None:
            self._draw_text("CAMARA", (panel.centerx, panel.y + 55), WHITE, self.small_font)
            self._draw_text("SIN SEÑAL", (panel.centerx, panel.y + 82), GOLD, self.small_font)
        else:
            self.screen.blit(preview, (panel.x + 4, panel.y + 4))
            pygame.draw.rect(
                self.screen,
                (235, 155, 74),
                (panel.x + 4, panel.y + 4, *CAMERA_PREVIEW_SIZE),
                2,
            )
        pygame.draw.rect(self.screen, (183, 103, 55), panel, 2)
        self._draw_text(
            "ESPEJO · PUNTOS",
            (panel.centerx, panel.bottom - 12),
            GOLD,
            self.small_font,
        )

    def _draw_overlay(self, title: str, subtitle: str, hint: str) -> None:
        """Dibuja un cuadro centrado para avisos, pausa o fin de partida."""
        self._panel(pygame.Rect(175, 230, 610, 245), (14, 9, 14, 228))
        pygame.draw.rect(self.screen, (180, 74, 45), (175, 230, 610, 245), 3)
        self._draw_text(title, (WIDTH // 2, 300), GOLD, self.title_font)
        self._draw_text(subtitle, (WIDTH // 2, 365), WHITE, self.font)
        self._draw_text(hint, (WIDTH // 2, 420), GOLD, self.small_font)

    def _draw_boss_end_overlay(
        self, title: str, subtitle: str, button_label: str
    ) -> None:
        """Muestra el resultado y la accion siguiente debajo del jefe."""
        panel = pygame.Rect(155, 500, 650, 155)
        self._panel(panel, (12, 0, 7, 235))
        pygame.draw.rect(self.screen, (174, 28, 42), panel, 3)
        self._draw_text(title, (WIDTH // 2, 535), GOLD, self.title_font)
        self._draw_text(subtitle, (WIDTH // 2, 579), WHITE, self.small_font)
        hovered = self.next_level_button.collidepoint(self._logical_mouse_position())
        self._panel(
            self.next_level_button,
            (105, 25, 30, 245) if hovered else (59, 20, 24, 235),
        )
        pygame.draw.rect(
            self.screen,
            GOLD if hovered else (183, 103, 55),
            self.next_level_button,
            2,
        )
        self._draw_text(
            button_label,
            self.next_level_button.center,
            WHITE,
            self.small_font,
        )

    def _wrap_story_text(self, text: str, max_width: int) -> list[str]:
        """Ajusta el relato a líneas que caben en la pantalla."""
        lines: list[str] = []
        current = ""
        for word in text.split():
            candidate = f"{current} {word}".strip()
            if current and self.story_body_font.size(candidate)[0] > max_width:
                lines.append(current)
                current = word
            else:
                current = candidate
        if current:
            lines.append(current)
        return lines

    def _draw_story_screen(self) -> None:
        """Presenta la crónica en negro con tipografía serif original y dramática."""
        self.screen.fill((0, 0, 0))
        story_red = (235, 48, 42)
        story_shadow = (89, 15, 20)
        pygame.draw.line(self.screen, (157, 26, 31), (150, 152), (810, 152), 2)
        self._draw_text(
            "CRÓNICA DE ASTER",
            (WIDTH // 2, 118),
            story_red,
            self.story_kicker_font,
        )
        self._draw_text(
            LEVEL_NAMES[self.level - 1].upper(),
            (WIDTH // 2 + 2, 213),
            story_shadow,
            self.story_title_font,
        )
        self._draw_text(
            LEVEL_NAMES[self.level - 1].upper(),
            (WIDTH // 2, 211),
            story_red,
            self.story_title_font,
        )
        visible_text = self.story_text[: self.story_revealed_chars]
        lines = self._wrap_story_text(visible_text, 760)
        for index, line in enumerate(lines):
            position = (WIDTH // 2, 310 + index * 48)
            self._draw_text(
                line,
                (position[0] + 2, position[1] + 2),
                story_shadow,
                self.story_body_font,
            )
            self._draw_text(line, position, story_red, self.story_body_font)

        story_revealed = self.story_revealed_chars >= len(self.story_text)
        button_label = (
            "SIGUIENTE MUNDO"
            if story_revealed and self.level < len(LEVEL_NAMES)
            else "VER DESENLACE"
            if story_revealed
            else "REVELAR HISTORIA"
        )
        hovered = self.next_level_button.collidepoint(self._logical_mouse_position())
        self._panel(
            self.next_level_button,
            (105, 25, 30, 245) if hovered else (59, 20, 24, 235),
        )
        pygame.draw.rect(
            self.screen,
            GOLD if hovered else (183, 103, 55),
            self.next_level_button,
            2,
        )
        self._draw_text(
            button_label,
            self.next_level_button.center,
            WHITE,
            self.small_font,
        )
        self._draw_text(
            "ENTER: revelar / continuar  ·  ESC: elegir mundo",
            (WIDTH // 2, 664),
            (190, 165, 139),
            self.tiny_font,
        )

    def _draw_pause_menu(self) -> None:
        """Muestra el botón PLAY; el estado del juego se conserva mientras está pausado."""
        self._draw_game()
        panel = pygame.Rect(175, 225, 610, 300)
        self._panel(panel, (12, 0, 7, 235))
        pygame.draw.rect(self.screen, (174, 28, 42), panel, 3)
        self._draw_text("PAUSA", (WIDTH // 2, 284), GOLD, self.title_font)
        self._draw_text("Tu partida está guardada.", (WIDTH // 2, 334), WHITE, self.font)
        hovered = self.pause_resume_button.collidepoint(
            self._logical_mouse_position()
        )
        fill = (112, 26, 34, 245) if hovered else (67, 15, 24, 240)
        self._panel(self.pause_resume_button, fill)
        pygame.draw.rect(
            self.screen,
            GOLD if hovered else (183, 103, 55),
            self.pause_resume_button,
            2,
        )
        self._draw_text(
            "PLAY / CONTINUAR",
            self.pause_resume_button.center,
            WHITE,
            self.font,
        )
        self._draw_text(
            "Haz clic o presiona ESC para seguir · M para menú",
            (WIDTH // 2, 475),
            GOLD,
            self.small_font,
        )

    def _draw_final_victory(self, show_message: bool) -> None:
        """Presenta el arte final y, después, el mensaje de victoria de Aster."""
        self.screen.fill((0, 0, 0))
        self.screen.blit(
            self.victory_image,
            self.victory_image.get_rect(center=(WIDTH // 2, HEIGHT // 2)),
        )
        if not show_message:
            self._draw_text(
                f"ENTER PARA CONTINUAR · {math.ceil(self.victory_intro_timer)}",
                (WIDTH // 2, HEIGHT - 24),
                GOLD,
                self.small_font,
            )
            return

        panel = pygame.Rect(85, 65, 790, 220)
        self._panel(panel, (4, 5, 11, 222))
        pygame.draw.rect(self.screen, (218, 166, 91), panel, 2)
        self._draw_text("¡VICTORIA!", (WIDTH // 2, 118), GOLD, self.title_font)
        for index, line in enumerate(self._wrap_story_text(FINAL_VICTORY_MESSAGE, 740)):
            self._draw_text(
                line,
                (WIDTH // 2, 178 + index * 38),
                WHITE,
                self.story_body_font,
            )
        hovered = self.victory_menu_button.collidepoint(self._logical_mouse_position())
        self._panel(
            self.victory_menu_button,
            (105, 25, 30, 245) if hovered else (59, 20, 24, 235),
        )
        pygame.draw.rect(
            self.screen,
            GOLD if hovered else (183, 103, 55),
            self.victory_menu_button,
            2,
        )
        self._draw_text(
            "VOLVER AL MENU",
            self.victory_menu_button.center,
            WHITE,
            self.small_font,
        )

    def _draw(self) -> None:
        """Selecciona la pantalla actual y la presenta en ventana o pantalla completa."""
        if self.state == "menu":
            self._draw_menu()
        elif self.state == "level_select":
            self._draw_level_select()
        elif self.state == "intro":
            self._draw_intro()
        elif self.state == "instructions":
            self._draw_instructions()
        elif self.state == "playing":
            self._draw_game()
        elif self.state == "boss_intro":
            self._draw_game()
            self._draw_overlay(
                "¡LLEGA EL JEFE!",
                self.level_boss_name,
                "PREPARATE PARA LUCHAR",
            )
        elif self.state == "paused":
            self._draw_pause_menu()
        elif self.state == "score":
            self._draw_menu()
            self._draw_overlay("PUNTAJE", f"Mejor puntuación de esta partida: {self.best_score}", "ENTER o ESC para volver")
        elif self.state == "game_over":
            self._draw_game()
            if self.boss is not None:
                self._draw_boss_end_overlay(
                    "FIN DEL JUEGO",
                    f"Puntaje: {self.score}",
                    "VOLVER AL MENU",
                )
            else:
                self._draw_overlay("FIN DEL JUEGO", f"Puntaje: {self.score}", "ENTER para volver al menú")
        elif self.state == "level_complete":
            self._draw_story_screen()
        elif self.state == "victory_intro":
            self._draw_final_victory(show_message=False)
        elif self.state == "victory":
            self._draw_final_victory(show_message=True)
        if self.state not in (
            "instructions",
            "intro",
            "level_select",
            "level_complete",
            "victory_intro",
            "victory",
        ):
            self._draw_camera_preview()
        self._present()

    def _present(self) -> None:
        """Usa fondo.jpg en los margenes y centra el juego sin deformarlo."""
        display_size = self.display.get_size()
        if self._wallpaper_cache_size != display_size:
            wallpaper = self.images["frame"]
            scale = max(
                display_size[0] / wallpaper.get_width(),
                display_size[1] / wallpaper.get_height(),
            )
            size = (
                round(wallpaper.get_width() * scale),
                round(wallpaper.get_height() * scale),
            )
            self._wallpaper_cache = pygame.transform.smoothscale(wallpaper, size)
            self._wallpaper_cache_size = display_size
        if self.state == "level_complete":
            self.display.fill((0, 0, 0))
        else:
            self.display.blit(
                self._wallpaper_cache,
                self._wallpaper_cache.get_rect(
                    center=(display_size[0] // 2, display_size[1] // 2)
                ),
            )
        scale = min(
            display_size[0] / WIDTH,
            display_size[1] / HEIGHT,
        )
        viewport_size = (round(WIDTH * scale), round(HEIGHT * scale))
        self.viewport = pygame.Rect(
            (display_size[0] - viewport_size[0]) // 2,
            (display_size[1] - viewport_size[1]) // 2,
            *viewport_size,
        )
        frame = (
            self.screen
            if viewport_size == self.screen.get_size()
            else pygame.transform.scale(self.screen, viewport_size)
        )
        self.display.blit(frame, self.viewport)
        if self.state != "level_complete":
            pygame.draw.rect(self.display, (142, 25, 42), self.viewport, 2)
        pygame.display.flip()

    def _toggle_fullscreen(self) -> None:
        """Alterna el modo de ventana y el modo de pantalla completa."""
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.display = pygame.display.set_mode(
                self.windowed_size,
                pygame.RESIZABLE,
            )
        self._wallpaper_cache_size = None

    def _new_game(self) -> None:
        """Inicia directamente el primer nivel para pruebas y accesos rapidos."""
        self._start_level(1, reset_score=True)

    def _start_level(self, level: int, reset_score: bool = False) -> None:
        """Inicia cualquier mundo con vidas completas y sus recursos propios."""
        if not 1 <= level <= len(LEVEL_NAMES):
            raise ValueError(f"Nivel fuera de rango: {level}")
        if reset_score:
            self.score = 0
        self.level = level
        self.selected_level = level
        self.level_boss_name = LEVEL_BOSS_NAMES[level - 1]
        self.player_aura = LEVEL_PLAYER_AURAS[level - 1]
        self.boss_image = self.boss_images[level - 1]
        self.lives = 3
        self.player_health = PLAYER_MAX_HEALTH
        self.special_charges = 3
        self.player.center = (WIDTH // 2, HEIGHT - 78)
        self.bullets.clear()
        self.ray_effects.clear()
        self.boss = None
        self.invulnerability = 0.0
        self.player_cooldown = 0.0
        self.power_cooldowns = {"energy": 0.0, "poseidon": 0.0, "ares": 0.0}
        self.keyboard_freeze = False
        self.is_frozen = False
        total_enemies = math.prod(LEVEL_FORMATIONS[level - 1])
        first_wave = max(2, total_enemies // 6)
        second_wave = max(first_wave + 1, total_enemies // 3)
        self.wave_sizes = (first_wave, second_wave, total_enemies)
        self.wave_index = 0
        self.audio.play_music(f"level_{self.level}")
        self._start_wave()
        self.state = "playing"

    def _start_wave(self) -> None:
        """Crea la formación de la oleada actual sin perder disparos propios."""
        self.bullets = [bullet for bullet in self.bullets if bullet["friendly"]]
        self.enemies.clear()
        self.boss = None
        self.enemy_fire_timer = max(
            0.35,
            1.05 - self.level * 0.055 - self.wave_index * 0.08,
        )
        _, max_columns = LEVEL_FORMATIONS[self.level - 1]
        enemy_count = self.wave_sizes[self.wave_index]
        columns = min(max_columns, enemy_count)
        spacing = 80
        formation_width = (columns - 1) * spacing + 42
        # Mantiene espacio de movimiento a ambos lados, incluso en las oleadas grandes.
        playfield_width = PLAYFIELD_RIGHT - FORMATION_LEFT_LIMIT
        start_x = FORMATION_LEFT_LIMIT + (playfield_width - formation_width) // 2
        self.formation_speed = 48.0 + self.level * 17.0 + self.wave_index * 12.0
        self.formation_direction = 1
        self.formation_vertical_direction = 1
        self.enemies = [
            {
                "rect": pygame.Rect(
                    start_x + index % columns * spacing,
                    105 + index // columns * 60,
                    42,
                    42,
                ),
                "phase": random.random() * 6.28,
                "variant": (
                    index % 2
                    if self.level in LEVEL_EXTRA_ENEMY_SPRITE_FILES
                    else 0
                ),
            }
            for index in range(enemy_count)
        ]
        self.stage_enemy_count = len(self.enemies)

    def _advance_wave_or_start_boss(self) -> None:
        """Avanza a una oleada mayor y solo presenta al jefe al terminar la última."""
        if self.enemies or self.boss is not None:
            return
        if self.wave_index + 1 < len(self.wave_sizes):
            self.wave_index += 1
            self._start_wave()
        else:
            self._start_boss()

    def _start_boss(self) -> None:
        """Lanza el jefe correspondiente al mundo cuando cae su ultima oleada."""
        if self.boss is not None:
            return
        self.enemies.clear()
        self.bullets = [bullet for bullet in self.bullets if bullet["friendly"]]
        boss_health = 200 + self.level * 30
        self.boss = {
            "rect": pygame.Rect(WIDTH // 2 - 125, 92, 250, 230),
            "health": boss_health,
            "max_health": boss_health,
            "direction": 1,
            "shot_timer": 0.65,
            "music_phase": 0,
            "stun_timer": 0.0,
            "burn_timer": 0.0,
            "burn_tick": 0.0,
        }
        self.boss_intro_timer = 1.8
        if self.level == len(LEVEL_NAMES):
            self.audio.play_music("boss_phase_1")
        self.state = "boss_intro"

    def _start_intro(self) -> None:
        """Abre el video del proyecto, sincronizando imagen y audio originales."""
        import imageio_ffmpeg

        video_path = asset_path(INTRO_VIDEO_FILE)
        self.intro_frames = imageio_ffmpeg.read_frames(str(video_path), pix_fmt="rgb24")
        metadata = next(self.intro_frames)
        self.intro_frame_size = metadata["size"]
        self.intro_fps = max(float(metadata["fps"]), 1.0)
        self.intro_accumulator = 1.0 / self.intro_fps
        self.intro_frame_surface = None
        self.state = "intro"
        self._update_intro(0.0)
        self.audio.play_intro_audio()

    def _update_intro(self, dt: float) -> None:
        """Decodifica los cuadros a su ritmo y comienza el nivel al terminar."""
        if self.intro_frames is None:
            return
        frame_duration = 1.0 / self.intro_fps
        self.intro_accumulator += dt
        while self.intro_accumulator >= frame_duration:
            self.intro_accumulator -= frame_duration
            try:
                frame_bytes = next(self.intro_frames)
            except StopIteration:
                self._finish_intro()
                return
            self.intro_frame_surface = pygame.image.frombuffer(
                frame_bytes, self.intro_frame_size, "RGB"
            ).copy()

    def _finish_intro(self) -> None:
        """Cierra el decodificador y comienza el primer nivel con vidas completas."""
        if self.intro_frames is not None:
            self.intro_frames.close()
            self.intro_frames = None
        self._start_level(1, reset_score=True)

    def _update_boss_intro(self, dt: float) -> None:
        """Da un breve aviso cinematografico antes de que el jefe ataque."""
        self.boss_intro_timer = max(0.0, self.boss_intro_timer - dt)
        if self.boss_intro_timer == 0:
            self.state = "playing"

    def _update_story(self, dt: float) -> None:
        """Revela lentamente la crónica al terminar cada mundo."""
        self.story_reveal_progress += dt * 48
        self.story_revealed_chars = min(
            len(self.story_text),
            int(self.story_reveal_progress),
        )

    def _start_victory_intro(self) -> None:
        """Inicia diez segundos de arte y música antes de revelar el mensaje final."""
        self.victory_intro_timer = VICTORY_INTRO_SECONDS
        self.state = "victory_intro"
        self.audio.play_music("victory")

    def _update_victory_intro(self, dt: float) -> None:
        """Avanza automáticamente al mensaje de victoria cuando termina la espera."""
        self.victory_intro_timer = max(0.0, self.victory_intro_timer - dt)
        if self.victory_intro_timer == 0:
            self._show_victory_message()

    def _show_victory_message(self) -> None:
        """Muestra el mensaje final tras la espera o la confirmación del jugador."""
        self.victory_intro_timer = 0.0
        self.state = "victory"

    def _reveal_story(self) -> None:
        """Muestra el relato completo al pulsar ENTER durante la animación."""
        self.story_revealed_chars = len(self.story_text)
        self.story_reveal_progress = float(self.story_revealed_chars)

    def _advance_story(self) -> None:
        """Continúa la campaña después de leer el relato del mundo."""
        if self.level < len(LEVEL_NAMES):
            self._start_level(self.level + 1)
        else:
            self._start_victory_intro()

    def _fire_player_bullet(self) -> None:
        """Crea un disparo vertical del jugador y activa su tiempo de recarga."""
        self.bullets.append(
            {
                "rect": pygame.Rect(self.player.centerx - 4, self.player.top - 13, 8, 20),
                "speed": -560,
                "x_speed": 0,
                "friendly": True,
                "color": (255, 220, 118),
            }
        )
        self.player_cooldown = 0.22

    def _fire_enemy_bullet(
        self, x: int, y: int, speed: float = 270, x_speed: float = 0
    ) -> None:
        """Añade un proyectil enemigo que cae hacia la nave del jugador."""
        self.bullets.append(
            {
                "rect": pygame.Rect(x - 5, y, 10, 18),
                "speed": speed,
                "x_speed": x_speed,
                "friendly": False,
                "color": (255, 82, 67),
            }
        )

    def _activate_zeus(self) -> None:
        """Gasta una carga del rayo de Zeus para limpiar enemigos o herir al jefe."""
        if self.special_charges <= 0:
            return
        self.special_charges -= 1
        self.audio.play_zeus()
        if self.boss is not None:
            self._add_ray_effect([self.boss["rect"].center], duration=0.55)
            self._damage_boss(60)
            self.score += 500
        elif self.enemies:
            targets = [enemy["rect"].center for enemy in self.enemies[:12]]
            self._add_ray_effect(targets, duration=0.55)
            self.score += 100 * len(self.enemies)
            self.enemies.clear()
            self._advance_wave_or_start_boss()

    def _add_ray_effect(
        self,
        targets: list[tuple[int, int]],
        duration: float = 0.38,
    ) -> None:
        """Calcula una vez los rayos dentados y conserva sus puntos para dibujarlos."""
        if targets:
            start_x, start_y = self.player.centerx, self.player.top
            rays: list[list[tuple[int, int]]] = []
            for end_x, end_y in targets:
                delta_x = end_x - start_x
                delta_y = end_y - start_y
                length = max(1.0, math.hypot(delta_x, delta_y))
                normal_x = -delta_y / length
                normal_y = delta_x / length
                points = [(start_x, start_y)]
                for step in range(1, 8):
                    fraction = step / 8
                    jitter = random.randint(-18, 18)
                    points.append(
                        (
                            round(start_x + delta_x * fraction + normal_x * jitter),
                            round(start_y + delta_y * fraction + normal_y * jitter),
                        )
                    )
                points.append((end_x, end_y))
                rays.append(points)
            self.ray_effects.append(
                {
                    "rays": rays,
                    "remaining": duration,
                }
            )

    def _fire_ray_volley(self) -> None:
        """Libera energia en varios rayos, con enfriamiento para equilibrar el poder."""
        if self.power_cooldowns["energy"] > 0:
            return
        self.power_cooldowns["energy"] = 2.2
        if self.boss is not None:
            boss_center = self.boss["rect"].center
            targets = [
                (boss_center[0] + offset, boss_center[1])
                for offset in (-70, -35, 0, 35, 70)
            ]
            self._add_ray_effect(targets)
            self._damage_boss(45)
            self.score += 250
            return

        if not self.enemies:
            return
        targets = sorted(
            self.enemies,
            key=lambda enemy: abs(enemy["rect"].centerx - self.player.centerx),
        )[:8]
        self._add_ray_effect([enemy["rect"].center for enemy in targets])
        for enemy in targets:
            self.enemies.remove(enemy)
        self.score += 100 * len(targets)
        if not self.enemies:
            self._advance_wave_or_start_boss()

    def _activate_poseidon(self) -> None:
        """Lanza una ola que derriba enemigos y aturde al guardian."""
        if self.power_cooldowns["poseidon"] > 0:
            return
        self.power_cooldowns["poseidon"] = 7.0
        if self.boss is not None:
            self._damage_boss(85)
            if self.boss is not None and self.state in ("playing", "boss_intro"):
                self.boss["stun_timer"] = max(self.boss["stun_timer"], 1.4)
            return
        self._remove_enemy_targets(10)

    def _activate_ares(self) -> None:
        """Desata una llamarada que consume enemigos y quema al guardian."""
        if self.power_cooldowns["ares"] > 0:
            return
        self.power_cooldowns["ares"] = 8.0
        if self.boss is not None:
            self._damage_boss(75)
            if self.boss is not None and self.state in ("playing", "boss_intro"):
                self.boss["burn_timer"] = max(self.boss["burn_timer"], 4.0)
                self.boss["burn_tick"] = 0.0
            return
        self._remove_enemy_targets(14)

    def _remove_enemy_targets(self, limit: int) -> None:
        """Retira hasta el limite de enemigos y abre la arena del jefe al final."""
        targets = sorted(
            self.enemies,
            key=lambda enemy: abs(enemy["rect"].centerx - self.player.centerx),
        )[:limit]
        for enemy in targets:
            self.enemies.remove(enemy)
        self.score += 100 * len(targets)
        if not self.enemies and targets:
            self._advance_wave_or_start_boss()

    def _damage_boss(self, amount: int) -> None:
        """Aplica daño una sola vez y conserva el flujo de victoria por nivel."""
        if self.boss is None:
            return
        self.boss["health"] = max(0, self.boss["health"] - amount)
        if self.boss["health"] == 0:
            self._win()

    def _take_damage(self) -> None:
        """Reduce la salud del jugador y descuenta una vida al agotarla."""
        if self.invulnerability > 0:
            return
        self.player_health = max(
            0,
            self.player_health - PLAYER_BULLET_DAMAGE,
        )
        if self.player_health == 0:
            self._lose_life()
        else:
            self.invulnerability = PLAYER_HIT_INVULNERABILITY

    def _lose_life(self) -> None:
        """Resta una vida, repone salud y concede protección temporal."""
        self.lives -= 1
        self.player_health = PLAYER_MAX_HEALTH
        self.invulnerability = 1.6
        if self.lives <= 0:
            self.best_score = max(self.best_score, self.score)
            self.state = "game_over"

    def _win(self) -> None:
        """Completa el mundo y prepara su crónica o el final de la campaña."""
        self.best_score = max(self.best_score, self.score)
        self.bullets = [bullet for bullet in self.bullets if bullet["friendly"]]
        if self.level == len(LEVEL_NAMES):
            self._start_victory_intro()
            return
        self.story_text = LEVEL_STORIES[self.level - 1]
        self.story_revealed_chars = 0
        self.story_reveal_progress = 0.0
        self.state = "level_complete"

    def _update_playing(
        self,
        dt: float,
        keys: pygame.key.ScancodeWrapper,
        hand_input: HandInput,
    ) -> None:
        """Mueve al jugador y actualiza disparos, enemigos y colisiones."""
        keyboard_x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(
            keys[pygame.K_LEFT] or keys[pygame.K_a]
        )
        movement_x = max(-1, min(1, keyboard_x + hand_input.move_x))
        movement_y = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(
            keys[pygame.K_UP] or keys[pygame.K_w]
        )
        was_frozen = self.is_frozen
        self.is_frozen = hand_input.freeze_active or self.keyboard_freeze
        if self.is_frozen and not was_frozen and self.boss is not None:
            self._damage_boss(15)
            if self.boss is not None:
                self.boss["stun_timer"] = max(self.boss["stun_timer"], 1.0)
        self.player.x += round(movement_x * 360 * dt)
        self.player.y += round(movement_y * 360 * dt)
        self.player.clamp_ip(
            pygame.Rect(
                PLAYFIELD_LEFT,
                PLAYFIELD_TOP,
                PLAYFIELD_RIGHT - PLAYFIELD_LEFT,
                PLAYFIELD_BOTTOM - PLAYFIELD_TOP,
            )
        )
        self.player_cooldown = max(0.0, self.player_cooldown - dt)
        self.invulnerability = max(0.0, self.invulnerability - dt)
        for name in self.power_cooldowns:
            self.power_cooldowns[name] = max(0.0, self.power_cooldowns[name] - dt)

        shooting = bool(keys[pygame.K_SPACE] or hand_input.shooting)
        self.audio.set_shooting_active(shooting)
        if shooting and self.player_cooldown == 0:
            self._fire_player_bullet()

        if self.boss is None:
            self._update_enemies(dt, self.is_frozen)
        else:
            self._update_boss(dt, self.is_frozen)
        self._update_bullets(dt)

    def _update_enemies(self, dt: float, frozen: bool = False) -> None:
        """Desplaza la formación, rebota en los bordes y elige quién dispara."""
        if not self.enemies:
            self._advance_wave_or_start_boss()
            return
        if frozen:
            return

        left_edge = min(enemy["rect"].left for enemy in self.enemies)
        right_edge = max(enemy["rect"].right for enemy in self.enemies)
        horizontal_step = round(self.formation_direction * self.formation_speed * dt)
        next_left = left_edge + horizontal_step
        next_right = right_edge + horizontal_step
        bounced = False
        if next_left < FORMATION_LEFT_LIMIT or (
            self.formation_direction < 0 and next_left <= FORMATION_LEFT_LIMIT
        ):
            horizontal_step = FORMATION_LEFT_LIMIT - left_edge
            self.formation_direction = 1
            bounced = True
        elif next_right > PLAYFIELD_RIGHT or (
            self.formation_direction > 0 and next_right >= PLAYFIELD_RIGHT
        ):
            horizontal_step = PLAYFIELD_RIGHT - right_edge
            self.formation_direction = -1
            bounced = True

        if bounced:
            lowest_bottom = max(enemy["rect"].bottom for enemy in self.enemies)
            highest_top = min(enemy["rect"].top for enemy in self.enemies)
            if self.formation_vertical_direction > 0:
                vertical_step = min(15, max(0, FORMATION_BOTTOM_LIMIT - lowest_bottom))
                if lowest_bottom + vertical_step >= FORMATION_BOTTOM_LIMIT:
                    self.formation_vertical_direction = -1
            else:
                available_ascent = max(0, highest_top - PLAYFIELD_TOP)
                if available_ascent == 0:
                    self.formation_vertical_direction = 1
                    vertical_step = min(
                        15,
                        max(0, FORMATION_BOTTOM_LIMIT - lowest_bottom),
                    )
                else:
                    vertical_step = -min(75, available_ascent)
                    if available_ascent <= 75:
                        self.formation_vertical_direction = 1
            for enemy in self.enemies:
                enemy["rect"].y += vertical_step

        for enemy in self.enemies:
            enemy["rect"].x += horizontal_step
            enemy["phase"] += dt * 3

        self.enemy_fire_timer -= dt
        if self.enemy_fire_timer <= 0:
            shooter = random.choice(self.enemies)
            speed = 220 + self.level * 15
            if self.level >= 8:
                for x_speed in (-72, 0, 72):
                    self._fire_enemy_bullet(
                        shooter["rect"].centerx,
                        shooter["rect"].bottom,
                        speed,
                        x_speed,
                    )
            else:
                self._fire_enemy_bullet(
                    shooter["rect"].centerx, shooter["rect"].bottom, speed
                )
            self.enemy_fire_timer = max(0.24, 1.05 - self.level * 0.085)

    def _update_boss(self, dt: float, frozen: bool = False) -> None:
        """Actualiza los estados, el desplazamiento y los ataques del guardian."""
        if self.boss is None:
            return
        self.boss["stun_timer"] = max(0.0, self.boss["stun_timer"] - dt)
        self.boss["burn_timer"] = max(0.0, self.boss["burn_timer"] - dt)
        if self.boss["burn_timer"] > 0:
            self.boss["burn_tick"] -= dt
            if self.boss["burn_tick"] <= 0:
                self._damage_boss(9)
                if self.boss is None or self.state != "playing":
                    return
                self.boss["burn_tick"] = 0.75
        if frozen or self.boss["stun_timer"] > 0:
            return
        boss_rect = self.boss["rect"]
        boss_left_limit = 115
        boss_right_limit = WIDTH - 115 - boss_rect.width
        next_x = boss_rect.x + round(self.boss["direction"] * 145 * dt)
        if next_x <= boss_left_limit:
            boss_rect.x = boss_left_limit
            self.boss["direction"] = 1
        elif next_x >= boss_right_limit:
            boss_rect.x = boss_right_limit
            self.boss["direction"] = -1
        else:
            boss_rect.x = next_x
        health_ratio = self.boss["health"] / self.boss["max_health"]
        phase = 2 if health_ratio <= 1 / 3 else 1 if health_ratio <= 2 / 3 else 0
        if phase != self.boss["music_phase"]:
            self.boss["music_phase"] = phase
            if phase and self.level == len(LEVEL_NAMES):
                self.audio.play_music(f"boss_phase_{phase + 1}")
        self.boss["shot_timer"] -= dt
        if self.boss["shot_timer"] <= 0:
            if self.boss["music_phase"] == 2:
                for x_speed in (-120, -60, 0, 60, 120):
                    self._fire_enemy_bullet(
                        boss_rect.centerx, boss_rect.bottom, 350, x_speed
                    )
            else:
                for offset in (-66, 0, 66):
                    self._fire_enemy_bullet(
                        boss_rect.centerx + offset,
                        boss_rect.bottom,
                        285 + self.level * 8,
                    )
            self.boss["shot_timer"] = 0.72 if self.boss["music_phase"] else 0.9

    def _update_bullets(self, dt: float) -> None:
        """Avanza cada proyectil, elimina los que salen y procesa sus impactos."""
        killed_enemy = False
        for bullet in self.bullets[:]:
            bullet["rect"].x += round(bullet.get("x_speed", 0) * dt)
            bullet["rect"].y += round(bullet["speed"] * dt)
            outside_playfield = not bullet["friendly"] and (
                bullet["rect"].right < PLAYFIELD_LEFT
                or bullet["rect"].left > PLAYFIELD_RIGHT
            )
            if (
                bullet["rect"].bottom < 0
                or bullet["rect"].top > HEIGHT
                or outside_playfield
            ):
                self.bullets.remove(bullet)
                continue
            if bullet["friendly"]:
                if self.boss is not None and bullet["rect"].colliderect(self.boss["rect"]):
                    self._damage_boss(4)
                    self.score += 10
                    self.bullets.remove(bullet)
                    continue
                hit = next(
                    (
                        enemy
                        for enemy in self.enemies
                        if bullet["rect"].colliderect(enemy["rect"])
                    ),
                    None,
                )
                if hit is not None:
                    self.enemies.remove(hit)
                    self.bullets.remove(bullet)
                    self.score += 100
                    killed_enemy = True
            elif bullet["rect"].colliderect(self.player):
                self.bullets.remove(bullet)
                self._take_damage()
        if killed_enemy and not self.enemies and self.boss is None:
            self._advance_wave_or_start_boss()

    def _handle_menu_click(self, position: tuple[int, int]) -> bool:
        """Activa la opción de menú situada bajo el clic."""
        if self.fullscreen_toggle_button.collidepoint(position):
            self.audio.play_ui_click()
            self._toggle_fullscreen()
            return True
        for index, (rect, _) in enumerate(self.menu_buttons):
            if rect.collidepoint(position):
                self.audio.play_ui_click()
                if index == 0:
                    self._start_intro()
                elif index == 1:
                    self.state = "level_select"
                elif index == 2:
                    self.state = "instructions"
                elif index == 3:
                    self.state = "score"
                else:
                    return False
                return True
        return True

    def _return_to_menu(self) -> None:
        """Vuelve al menu y restaura el tema musical de portada."""
        self.state = "menu"
        self.audio.play_music("menu")

    def _start_selected_level(self, index: int) -> None:
        """Inicia el mundo seleccionado y conserva la selección para el menú."""
        self.selected_level = index
        self._start_level(index, reset_score=True)

    def _handle_event(self, event: pygame.event.Event) -> bool:
        """Convierte eventos de ratón y teclado en cambios de estado o acciones."""
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.VIDEORESIZE and not self.fullscreen:
            self.windowed_size = (
                max(MIN_WINDOW_SIZE[0], event.w),
                max(MIN_WINDOW_SIZE[1], event.h),
            )
            self.display = pygame.display.set_mode(
                self.windowed_size,
                pygame.RESIZABLE,
            )
            self._wallpaper_cache_size = None
            return True
        if event.type == pygame.KEYUP:
            self.keyboard_power_keys_down.discard(event.key)
            return True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Los clics se convierten al tamaño lógico, incluso con barras laterales.
            position = (
                round((event.pos[0] - self.viewport.x) * WIDTH / self.viewport.width),
                round((event.pos[1] - self.viewport.y) * HEIGHT / self.viewport.height),
            )
            if self.state == "menu":
                return self._handle_menu_click(position)
            if self.state == "level_select":
                for index, rect in enumerate(self.level_buttons, start=1):
                    if rect.collidepoint(position):
                        self.audio.play_ui_click()
                        self._start_selected_level(index)
                        break
            elif self.state == "instructions":
                self.audio.play_ui_click()
                self.state = "menu"
            elif self.state == "paused" and self.pause_resume_button.collidepoint(position):
                self.audio.play_ui_click()
                self._resume_game()
            elif self.state == "victory_intro":
                self.audio.play_ui_click()
                self._show_victory_message()
            elif self.state == "level_complete" and self.next_level_button.collidepoint(position):
                self.audio.play_ui_click()
                if self.story_revealed_chars < len(self.story_text):
                    self._reveal_story()
                else:
                    self._advance_story()
            elif self.state == "victory" and self.victory_menu_button.collidepoint(position):
                self.audio.play_ui_click()
                self._return_to_menu()
            elif self.state == "game_over" and self.next_level_button.collidepoint(position):
                self.audio.play_ui_click()
                self._return_to_menu()
            return True
        if event.type != pygame.KEYDOWN:
            return True
        if event.key == pygame.K_F11:
            self._toggle_fullscreen()
            return True
        if event.key == pygame.K_v:
            self.show_camera_preview = not self.show_camera_preview
            return True

        if self.state == "intro":
            if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                self._finish_intro()
        elif self.state == "menu":
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._start_intro()
            elif event.key in (pygame.K_n, pygame.K_l):
                self.state = "level_select"
            elif event.key == pygame.K_i:
                self.state = "instructions"
            elif event.key == pygame.K_p:
                self.state = "score"
            elif event.key == pygame.K_ESCAPE:
                return False
        elif self.state == "level_select":
            level_keys = {
                pygame.K_1: 1,
                pygame.K_2: 2,
                pygame.K_3: 3,
                pygame.K_4: 4,
                pygame.K_5: 5,
                pygame.K_6: 6,
                pygame.K_7: 7,
                pygame.K_8: 8,
                pygame.K_9: 9,
                pygame.K_0: 10,
            }
            if event.key in level_keys:
                self._start_selected_level(level_keys[event.key])
            elif event.key == pygame.K_ESCAPE:
                self._return_to_menu()
        elif self.state == "instructions":
            if event.key in (pygame.K_RETURN, pygame.K_ESCAPE, pygame.K_BACKSPACE):
                self._return_to_menu()
        elif self.state == "playing":
            if event.key in self.keyboard_power_keys:
                self.keyboard_power_keys_down.add(event.key)
            if event.key == pygame.K_ESCAPE:
                self.state = "paused"
                pygame.mixer.music.pause()
            elif event.key == pygame.K_e:
                self._activate_zeus()
            elif event.key == pygame.K_1:
                self._activate_zeus()
            elif event.key == pygame.K_2:
                self.keyboard_freeze = not self.keyboard_freeze
            elif event.key == pygame.K_3:
                self._fire_ray_volley()
            elif event.key == pygame.K_4:
                self._activate_poseidon()
            elif event.key == pygame.K_5:
                self._activate_ares()
        elif self.state == "boss_intro":
            if event.key == pygame.K_RETURN:
                self.boss_intro_timer = 0.0
                self.state = "playing"
        elif self.state == "paused":
            if event.key == pygame.K_ESCAPE:
                self._resume_game()
            elif event.key == pygame.K_m:
                self._return_to_menu()
        elif self.state == "level_complete":
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                if self.story_revealed_chars < len(self.story_text):
                    self._reveal_story()
                else:
                    self._advance_story()
            elif event.key == pygame.K_ESCAPE:
                self.selected_level = self.level
                self.state = "level_select"
                self.audio.play_music("menu")
        elif self.state == "victory_intro":
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._show_victory_message()
        elif self.state in ("score", "game_over", "victory"):
            if event.key in (pygame.K_RETURN, pygame.K_ESCAPE, pygame.K_SPACE):
                self._return_to_menu()
        return True

    def _resume_game(self) -> None:
        """Reanuda la partida pausada sin reiniciar su progreso."""
        self.state = "playing"
        pygame.mixer.music.unpause()

    def _apply_hand_actions(self, hand_input: HandInput) -> None:
        """Aplica las acciones de un gesto una sola vez cuando corresponde."""
        if hand_input.pause_pressed:
            if self.state == "playing":
                self.state = "paused"
                pygame.mixer.music.pause()
            elif self.state == "paused":
                self._resume_game()
        if self.state == "playing":
            if hand_input.lightning_pressed:
                self._activate_zeus()
            if hand_input.energy_pressed:
                self._fire_ray_volley()
            if hand_input.poseidon_pressed:
                self._activate_poseidon()
            if hand_input.ares_pressed:
                self._activate_ares()

    def _sync_power_feedback(self, hand_input: HandInput) -> None:
        """Sincroniza audio e ilustraciones con los gestos y teclas sostenidos."""
        desired: set[str] = set()
        if self.state == "playing":
            desired.update(hand_input.active_powers)
            desired.update(
                self.keyboard_power_keys[key]
                for key in self.keyboard_power_keys_down
                if key in self.keyboard_power_keys
            )
            if self.keyboard_freeze:
                desired.add("freeze")

        for name in self.active_powers - desired:
            self.audio.set_power_active(name, False)
        for name in desired - self.active_powers:
            self.audio.set_power_active(name, True)
        self.active_powers = desired

    def _update_ray_effects(self, dt: float) -> None:
        """Reduce el tiempo de los rayos y retira los efectos ya terminados."""
        for effect in self.ray_effects:
            effect["remaining"] -= dt
        self.ray_effects = [
            effect for effect in self.ray_effects if effect["remaining"] > 0
        ]

    def run(self) -> None:
        """Ejecuta el ciclo principal: cámara, eventos, simulación y dibujo."""
        running = True
        while running:
            dt = min(self.clock.tick(FPS) / 1000.0, 0.05)
            # Se procesa un cuadro de cámara por iteración para mantener el control fluido.
            hand_input = (
                self.hand_controller.poll()
                if self.hand_controller is not None
                else HandInput()
            )
            for event in pygame.event.get():
                running = self._handle_event(event) and running
            if not running:
                break
            self._apply_hand_actions(hand_input)
            self._sync_power_feedback(hand_input)
            self._update_ray_effects(dt)
            if self.state == "intro":
                self._update_intro(dt)
            elif self.state == "boss_intro":
                self._update_boss_intro(dt)
            elif self.state == "level_complete":
                self._update_story(dt)
            elif self.state == "victory_intro":
                self._update_victory_intro(dt)
            if self.state == "playing":
                self._update_playing(dt, pygame.key.get_pressed(), hand_input)
            else:
                self.audio.set_shooting_active(False)
            self._draw()
        self.close()

    def close(self) -> None:
        """Cierra cámara, audio y Pygame al salir de la aplicación."""
        if self.intro_frames is not None:
            self.intro_frames.close()
            self.intro_frames = None
        if self.hand_controller is not None:
            self.hand_controller.close()
        self.audio.close()
        pygame.quit()


def self_test() -> None:
    """Comprueba menu, video, niveles, poderes, camara y jefes."""
    import numpy as np
    from types import SimpleNamespace

    pygame.init()
    game = Game(use_camera=False)
    try:
        if game.fullscreen or game.display.get_size() != (WIDTH, HEIGHT):
            raise AssertionError("El juego no comenzó en una ventana pequeña.")
        game.audio.play_ui_click()
        if (
            not game.audio.ui_click_channel.get_busy()
            or game.audio.shot_channel.get_busy()
            or set(game.audio.effect_sounds) != {"button"}
            or abs(game.audio.effect_sounds["button"].get_volume() - 0.72) > 0.01
        ):
            raise AssertionError("El efecto de botón sonó o el láser se activó en reposo.")

        missing_assets = [
            str(path) for path in ASSET_PATHS.values() if not path.is_file()
        ]
        if missing_assets:
            raise AssertionError(f"Faltan recursos del juego: {missing_assets}")

        def screen_position(position: tuple[int, int]) -> tuple[int, int]:
            """Convierte una posición lógica de la interfaz a coordenadas de ventana."""
            return (
                game.viewport.x
                + round(position[0] * game.viewport.width / WIDTH),
                game.viewport.y
                + round(position[1] * game.viewport.height / HEIGHT),
            )

        gesture_cases = [
            ([False, True, False, False, False], "one"),
            ([False, True, True, False, False], "two"),
            ([False, True, True, True, False], "three"),
            ([False, True, True, True, True], "four"),
            ([True, True, True, True, True], "open"),
            ([False, False, False, False, False], "fist"),
        ]
        for fingers, expected in gesture_cases:
            if HandController._gesture_from_fingers(fingers) != expected:
                raise AssertionError(f"No se reconoció el gesto {expected}.")
        expected_renamed_tracks = {
            "menu": "sonido1.mp4",
            "level_7": "sonido6.mp4",
            "level_8": "sonido4.mp4",
            "level_9": "sonido8.mp4",
            "level_10": "sonido7.mp4",
            "boss_phase_1": "sonido3.mp4",
            "boss_phase_2": "sonido2.mp4",
            "boss_phase_3": "sonido5.mp4",
        }
        if any(
            MUSIC_FILES[name] != filename
            for name, filename in expected_renamed_tracks.items()
        ):
            raise AssertionError("Las canciones renombradas no tienen su asignación correcta.")

        class FakeCapture:
            """Cámara de prueba que siempre entrega el mismo cuadro sintético."""

            def __init__(self, frame: Any) -> None:
                """Conserva un cuadro de prueba en vez de abrir una cámara real."""
                self.frame = frame

            def read(self) -> tuple[bool, Any]:
                """Entrega una copia del cuadro para que el test pueda repetirlo."""
                return True, self.frame.copy()

            def release(self) -> None:
                """Mantiene la misma interfaz que VideoCapture sin liberar hardware."""
                return None

        landmarks = [SimpleNamespace(x=0.5, y=0.5) for _ in range(21)]
        landmarks[6].y = 0.6
        landmarks[8].y = 0.2
        hand = SimpleNamespace(landmark=landmarks)
        left_landmarks = [SimpleNamespace(x=0.5, y=0.5) for _ in range(21)]
        for tip, joint in ((8, 6), (12, 10), (16, 14)):
            left_landmarks[joint].y = 0.6
            left_landmarks[tip].y = 0.2
        left_hand = SimpleNamespace(landmark=left_landmarks)
        handedness = [
            SimpleNamespace(classification=[SimpleNamespace(label="Right")]),
            SimpleNamespace(classification=[SimpleNamespace(label="Left")]),
        ]
        fake_result = SimpleNamespace(
            multi_hand_landmarks=[hand, left_hand],
            multi_handedness=handedness,
        )
        fake_tracker = SimpleNamespace(
            process=lambda _: fake_result
        )
        camera = object.__new__(HandController)
        camera.capture = FakeCapture(
            np.concatenate(
                (
                    np.full((480, 320, 3), (0, 0, 255), dtype=np.uint8),
                    np.full((480, 320, 3), (255, 0, 0), dtype=np.uint8),
                ),
                axis=1,
            )
        )
        camera.camera_available = True
        camera.tracker = fake_tracker
        camera.preview_surface = None
        camera._candidates = {"Left": None, "Right": None}
        camera._stable = {"Left": None, "Right": None}
        camera._candidate_frames = {"Left": 0, "Right": 0}
        camera._missing_frames = {"Left": 0, "Right": 0}
        for _ in range(3):
            camera_input = camera.poll()
        if camera_input.move_x != -1:
            raise AssertionError("El gesto de índice derecho no movió la nave.")
        if camera_input.active_powers != {"energy"}:
            raise AssertionError("El gesto izquierdo no mantuvo el poder de energía.")
        if not camera_input.energy_pressed:
            raise AssertionError("El gesto izquierdo no activó el poder de energía.")
        if camera.preview_surface is None or camera.preview_surface.get_size() != CAMERA_PREVIEW_SIZE:
            raise AssertionError("No se creó la vista de cámara con puntos.")
        if camera.preview_surface.get_at((20, 60))[:3] != (0, 0, 255):
            raise AssertionError("La vista previa no está reflejada.")
        if camera.preview_surface.get_at((80, 60))[:3] != (255, 255, 0):
            raise AssertionError("No se resaltaron los puntos del gesto.")

        def set_right_fingers(extended: tuple[bool, bool, bool, bool]) -> None:
            """Prepara los puntos sintéticos de cuatro dedos de la mano derecha."""
            for is_extended, (tip, joint) in zip(
                extended,
                ((8, 6), (12, 10), (16, 14), (20, 18)),
            ):
                landmarks[joint].y = 0.6
                landmarks[tip].y = 0.2 if is_extended else 0.8

        def set_left_fingers(
            extended: tuple[bool, bool, bool, bool, bool],
            separated: bool = True,
        ) -> None:
            """Simula dedos levantados, con o sin separación lateral para Ares."""
            left_landmarks[3].x = 0.52
            left_landmarks[5].x = 0.42
            left_landmarks[17].x = 0.58
            if separated:
                tip_x = (0.24, 0.34, 0.44, 0.54, 0.68)
            else:
                tip_x = (0.40, 0.42, 0.44, 0.46, 0.48)
            left_landmarks[4].x = tip_x[0] if extended[0] else 0.8
            for is_extended, (tip, joint), tip_position in zip(
                extended[1:],
                ((8, 6), (12, 10), (16, 14), (20, 18)),
                tip_x[1:],
            ):
                left_landmarks[joint].y = 0.6
                left_landmarks[tip].y = 0.2 if is_extended else 0.8
                left_landmarks[tip].x = tip_position

        for fingers, expected_move, expected_pause, expected_shooting in (
            ((True, True, False, False), 1, False, False),
            ((True, True, True, False), 0, True, False),
            ((False, False, False, False), 0, False, True),
        ):
            set_right_fingers(fingers)
            for _ in range(3):
                camera_input = camera.poll()
            if (
                camera_input.move_x != expected_move
                or camera_input.pause_pressed != expected_pause
                or camera_input.shooting != expected_shooting
            ):
                raise AssertionError("No coinciden los gestos de movimiento, pausa y disparo.")
        fist_shot_input = camera_input

        set_left_fingers((True, True, True, True, True))
        for _ in range(3):
            camera_input = camera.poll()
        if camera_input.active_powers != {"ares"} or not camera_input.ares_pressed:
            raise AssertionError("ARES requiere la mano izquierda abierta con cinco dedos.")
        set_left_fingers((True, True, True, True, True), separated=False)
        for _ in range(3):
            camera_input = camera.poll()
        if camera_input.active_powers == {"ares"} or camera_input.ares_pressed:
            raise AssertionError("Los dedos juntos activaron por error el fuego de Ares.")
        set_left_fingers((False, True, True, True, True))
        for _ in range(3):
            camera_input = camera.poll()
        if camera_input.active_powers == {"ares"} or camera_input.ares_pressed:
            raise AssertionError("Cuatro dedos activaron por error el fuego de Ares.")

        fake_result.multi_hand_landmarks = None
        fake_result.multi_handedness = None
        for _ in range(6):
            camera_input = camera.poll()
        if camera_input.active_powers:
            raise AssertionError("El poder quedó activo al desaparecer la mano.")

        for track in MUSIC_FILES:
            game.audio.play_music(track)
        for power in POWER_SOUND_FILES:
            game.audio.play_power(power)
        game.audio.play_zeus()
        game._draw()
        game._handle_event(
            pygame.event.Event(
                pygame.MOUSEBUTTONDOWN,
                {"button": 1, "pos": screen_position(game.menu_buttons[0][0].center)},
            )
        )
        if (
            game.state != "intro"
            or game.intro_frame_surface is None
            or game.intro_frame_surface.get_size() != (1024, 576)
            or game.audio.intro_audio_path is None
        ):
            raise AssertionError("No se inicio el video con su audio original.")
        game._draw()
        game._handle_event(
            pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN})
        )
        if game.state != "playing" or game.level != 1 or game.lives != 3:
            raise AssertionError("ENTER no salto la intro e inicio el primer nivel.")
        game._sync_power_feedback(
            HandInput(active_powers=frozenset({"energy"}))
        )
        if (
            game.active_powers != {"energy"}
            or "energy" not in game.audio.active_power_sounds
            or not game.audio.power_channels["energy"].get_busy()
        ):
            raise AssertionError("El poder no sincronizo su sonido con el gesto.")
        previous_screen = game.screen
        effect_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        game.screen = effect_surface
        game._draw_power_effects()
        if effect_surface.get_bounding_rect(min_alpha=1).width == 0:
            raise AssertionError("El poder activo no mostro su imagen.")
        game._sync_power_feedback(HandInput())
        if (
            game.active_powers
            or "energy" in game.audio.active_power_sounds
            or game.audio.power_channels["energy"].get_busy()
        ):
            raise AssertionError("El sonido o la imagen no se detuvieron al soltarlo.")
        effect_surface.fill((0, 0, 0, 0))
        game._draw_power_effects()
        if effect_surface.get_bounding_rect(min_alpha=1).width != 0:
            raise AssertionError("La imagen del poder permanecio tras soltar el gesto.")
        game.screen = previous_screen
        game.enemies.clear()
        game._handle_event(
            pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_3})
        )
        game._sync_power_feedback(HandInput())
        if (
            "energy" not in game.active_powers
            or not game.audio.power_channels["energy"].get_busy()
        ):
            raise AssertionError("La tecla no mantuvo el poder de energía activo.")
        game._handle_event(pygame.event.Event(pygame.KEYUP, {"key": pygame.K_3}))
        game._sync_power_feedback(HandInput())
        if (
            "energy" in game.active_powers
            or game.audio.power_channels["energy"].get_busy()
        ):
            raise AssertionError("Soltar la tecla no detuvo el sonido del poder.")
        game._handle_event(
            pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_2})
        )
        game._sync_power_feedback(HandInput())
        if (
            not game.keyboard_freeze
            or "freeze" not in game.active_powers
            or not game.audio.power_channels["freeze"].get_busy()
        ):
            raise AssertionError("El congelamiento del teclado no activo sus efectos.")
        game._handle_event(pygame.event.Event(pygame.KEYUP, {"key": pygame.K_2}))
        game._sync_power_feedback(HandInput())
        if "freeze" not in game.active_powers:
            raise AssertionError("El congelamiento conmutado se apago al soltar la tecla.")
        game._handle_event(
            pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_2})
        )
        game._handle_event(pygame.event.Event(pygame.KEYUP, {"key": pygame.K_2}))
        game._sync_power_feedback(HandInput())
        if (
            game.keyboard_freeze
            or "freeze" in game.active_powers
            or game.audio.power_channels["freeze"].get_busy()
        ):
            raise AssertionError("El poder no se detuvo al desactivar el congelamiento.")
        expected_images = (
            len(ASSET_FILES)
            + len(LEVEL_ENEMY_SPRITE_FILES)
            + len(LEVEL_EXTRA_ENEMY_SPRITE_FILES)
            + len(LEVEL_BOSS_SPRITE_FILES)
            + len(POWER_IMAGE_FILES)
            + sum(len(files) for files in LEVEL_BACKGROUND_FILES)
        )
        if len(game.images) != expected_images:
            raise AssertionError("No se cargaron todas las imágenes del juego.")
        if (
            len(game.level_backgrounds) != 10
            or sum(map(len, game.level_backgrounds)) != 20
        ):
            raise AssertionError("Los diez niveles no cargaron todas las fotos nuevas.")
        if (
            game.player_image.get_at((0, 0)).a == 255
            or game.enemy_images[0].get_at((0, 0)).a == 255
            or len(game.boss_images) != 10
            or len(game.extra_enemy_images) != 1
            or LEVEL_NAMES[9] != "Mundo de Ares"
            or LEVEL_BOSS_NAMES[9] != "Ares, Señor del Caos"
        ):
            raise AssertionError("El nivel 10 no cargó el mundo y los sprites de Ares.")
        if len(game.audio.power_sounds) != len(POWER_SOUND_FILES):
            raise AssertionError("No se cargaron todos los sonidos de poderes.")
        if (
            game.power_effect_images["energy"].get_width() < 260
            or game.power_effect_images["lightning_aura"].get_width() < 250
            or any(
                game.power_effect_images[name].get_alpha() != 255
                for name in POWER_SOUND_FILES
            )
            or any(sound.get_volume() < 0.85 for sound in game.audio.power_sounds.values())
        ):
            raise AssertionError("Las imágenes de poder no conservan tamaño y color.")
        fallback = game._fallback_image("arena")
        if (
            fallback.get_size() != (WIDTH, HEIGHT)
            or fallback.get_at((8, 8))[:3] != (3, 0, 8)
            or fallback.get_at((WIDTH // 2, HEIGHT // 2))[:3] != (120, 10, 28)
        ):
            raise AssertionError("El fondo de respaldo no usa negro y rojo.")
        game._new_game()
        if game.level != 1 or game.wave_sizes != (2, 3, 8) or len(game.enemies) != 2:
            raise AssertionError("El primer nivel no comienza con pocos enemigos.")
        health_label = game.tiny_font.render("SALUD 100%", True, WHITE)
        status_label = game.tiny_font.render("VIDAS 3  PTS 000000", True, WHITE)
        health_label_rect = health_label.get_rect(center=(78, 80))
        status_label_rect = status_label.get_rect(center=(248, 78))
        if health_label_rect.colliderect(status_label_rect):
            raise AssertionError("La salud se superpone con vidas y puntaje en el HUD.")

        for enemy in game.enemies:
            enemy["rect"].bottom = FORMATION_BOTTOM_LIMIT - 15
        game.enemies[0]["rect"].left = FORMATION_LEFT_LIMIT
        game.formation_direction = -1
        game._update_enemies(0)
        if (
            max(enemy["rect"].bottom for enemy in game.enemies)
            != FORMATION_BOTTOM_LIMIT
            or game.formation_vertical_direction != -1
        ):
            raise AssertionError("La formación no invirtio el descenso a tiempo.")
        for index, enemy in enumerate(game.enemies):
            enemy["rect"].left = PLAYFIELD_RIGHT - 42 - index * 80
        game.formation_direction = 1
        game._update_enemies(0)
        if (
            max(enemy["rect"].bottom for enemy in game.enemies)
            != FORMATION_BOTTOM_LIMIT - 75
        ):
            raise AssertionError("La formación no regreso rapido desde el limite inferior.")

        game._start_level(10, reset_score=True)
        game.wave_index = len(game.wave_sizes) - 1
        game._start_wave()
        if min(enemy["rect"].left for enemy in game.enemies) < FORMATION_LEFT_LIMIT:
            raise AssertionError("La oleada grande comenzo fuera del margen horizontal.")
        horizontal_positions = []
        for _ in range(600):
            game._update_enemies(1 / FPS)
            horizontal_positions.append(game.enemies[0]["rect"].x)
        if (
            max(horizontal_positions) - min(horizontal_positions) < 100
            or min(enemy["rect"].left for enemy in game.enemies) < FORMATION_LEFT_LIMIT
            or max(enemy["rect"].right for enemy in game.enemies) > PLAYFIELD_RIGHT
            or min(enemy["rect"].top for enemy in game.enemies) < PLAYFIELD_TOP
            or max(enemy["rect"].bottom for enemy in game.enemies)
            > FORMATION_BOTTOM_LIMIT
        ):
            raise AssertionError("La oleada grande se atasco o salio de sus limites.")

        game._new_game()
        if game.player_health != PLAYER_MAX_HEALTH:
            raise AssertionError("El jugador no inicio el nivel con la salud completa.")
        game.bullets = [
            {
                "rect": game.player.copy(),
                "speed": 0,
                "x_speed": 0,
                "friendly": False,
                "color": RED,
            }
        ]
        game._update_bullets(0)
        if game.player_health != 75 or game.lives != 3:
            raise AssertionError("Un impacto quito una vida en vez de salud.")
        for expected_health in (50, 25):
            game.invulnerability = 0
            game._take_damage()
            if game.player_health != expected_health or game.lives != 3:
                raise AssertionError("La barra de salud no absorbio varios impactos.")
        game.invulnerability = 0
        game._take_damage()
        if game.player_health != PLAYER_MAX_HEALTH or game.lives != 2:
            raise AssertionError("La vida no se resto al vaciar la barra de salud.")

        game.player.right = PLAYFIELD_RIGHT
        previous_screen = game.screen
        health_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        game.screen = health_surface
        game._draw_player_health()
        health_bar = pygame.Rect(24, 48, 108, 13)
        power_tiles = [
            pygame.Rect(WIDTH - 86, 198 + index * 88, 72, 76)
            for index in range(5)
        ]
        if (
            health_surface.get_bounding_rect(min_alpha=1).width == 0
            or health_bar.colliderect(game.player)
            or any(tile.colliderect(game.player) for tile in power_tiles)
            or any(tile.colliderect(health_bar) for tile in power_tiles)
            or max(tile.bottom for tile in power_tiles) >= HEIGHT
        ):
            raise AssertionError("La interfaz lateral tapa al jugador o su salud.")
        game.lives = 2
        game.player_health = 25
        game._draw_game()
        normal_life_pixel = game.screen.get_at((420, 400))
        game.lives = 1
        game._draw_game()
        critical_life_pixel = game.screen.get_at((420, 400))
        if (
            normal_life_pixel == critical_life_pixel
            or critical_life_pixel.r <= normal_life_pixel.r
        ):
            raise AssertionError("La pantalla no aplica el filtro rojo en la última vida.")
        game.screen = previous_screen
        game._new_game()
        game._update_playing(0, pygame.key.get_pressed(), HandInput())
        if game.audio.shot_channel.get_busy() or "laser" in game.audio.effect_sounds:
            raise AssertionError("El láser sonó sin que la nave disparara.")
        game._update_playing(0, pygame.key.get_pressed(), fist_shot_input)
        if (
            not any(bullet["friendly"] for bullet in game.bullets)
            or not game.audio.shot_channel.get_busy()
            or abs(game.audio.effect_sounds["laser"].get_volume() - 0.35) > 0.01
        ):
            raise AssertionError("El puño derecho no disparó con su efecto de sonido.")
        game.audio.set_shooting_active(False)
        if game.audio.shot_channel.get_busy() or game.audio.shooting_active:
            raise AssertionError("El láser no se detuvo al soltar el disparo.")
        game._new_game()
        target = game.enemies[0]
        game.bullets = [
            {
                "rect": target["rect"].copy(),
                "speed": 0,
                "friendly": True,
                "color": GOLD,
            }
        ]
        game._update_bullets(0)
        if len(game.enemies) != game.wave_sizes[0] - 1 or game.score != 100:
            raise AssertionError("No se registró el impacto del jugador.")
        first_enemy_x = game.enemies[0]["rect"].x
        game._update_enemies(1.0, frozen=True)
        if game.enemies[0]["rect"].x != first_enemy_x:
            raise AssertionError("El gesto de congelamiento no detuvo la formación.")
        game._fire_ray_volley()
        if (
            game.level != 1
            or len(game.enemies) != game.wave_sizes[1]
            or game.wave_index != 1
            or game.boss is not None
            or game.state != "playing"
            or game.score != 200
            or not game.ray_effects
        ):
            raise AssertionError("La segunda oleada no aumento tras vencer a la primera.")
        game.enemies.clear()
        game._update_enemies(0)
        if len(game.enemies) != game.wave_sizes[2] or game.boss is not None:
            raise AssertionError("La tercera oleada no tuvo más enemigos.")
        game.enemies.clear()
        game._update_enemies(0)
        if game.boss is None or game.state != "boss_intro":
            raise AssertionError("El jefe no espero a que terminaran las oleadas.")

        paused_enemy_count = len(game.enemies)
        paused_player_position = game.player.topleft
        game.state = "paused"
        pygame.mixer.music.pause()
        game._draw()
        resume_click = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN,
            {"button": 1, "pos": screen_position(game.pause_resume_button.center)},
        )
        game._handle_event(resume_click)
        if (
            game.state != "playing"
            or len(game.enemies) != paused_enemy_count
            or game.player.topleft != paused_player_position
        ):
            raise AssertionError("PLAY no continuó la partida pausada.")

        game.hand_controller = SimpleNamespace(
            status_text="CAMARA ACTIVA",
            gesture_summary="DER: IZQ",
            preview_surface=pygame.Surface(CAMERA_PREVIEW_SIZE),
        )
        game._draw()
        game.hand_controller = None
        game.state = "menu"
        game._handle_event(
            pygame.event.Event(
                pygame.VIDEORESIZE,
                {"w": 1080, "h": 810},
            )
        )
        if game.display.get_size() != (1080, 810):
            raise AssertionError("La ventana no se pudo redimensionar.")
        game._draw()
        fullscreen_click = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN,
            {"button": 1, "pos": screen_position(game.fullscreen_toggle_button.center)},
        )
        game._handle_event(fullscreen_click)
        if not game.fullscreen:
            raise AssertionError("El botón no activó la pantalla completa.")
        game._draw()
        game._handle_event(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_F11}))
        display_flags = game.display.get_flags()
        if (
            game.fullscreen
            or game.windowed_size != (1080, 810)
            or not display_flags & pygame.RESIZABLE
            or display_flags & pygame.FULLSCREEN
        ):
            raise AssertionError("F11 no restauró la ventana redimensionada.")

        game._handle_event(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_n}))
        if game.state != "level_select":
            raise AssertionError("El menu no abrio la seleccion de mundos.")
        game._draw()
        game._handle_event(
            pygame.event.Event(
                pygame.MOUSEBUTTONDOWN,
                {"button": 1, "pos": screen_position(game.level_buttons[3].center)},
            )
        )
        if game.level != 4 or game.lives != 3:
            raise AssertionError("No se pudo elegir un mundo con el raton.")
        game._return_to_menu()
        game._handle_event(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_n}))
        game._handle_event(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_7}))
        if game.level != 7 or len(game.enemies) != game.wave_sizes[0] or game.lives != 3:
            raise AssertionError("No se pudo iniciar un nivel elegido con vidas completas.")
        game.lives = 1
        game._start_boss()
        game._damage_boss(game.boss["max_health"])
        if game.state != "level_complete":
            raise AssertionError("Vencer al jefe no completo el mundo seleccionado.")
        if game.story_text != LEVEL_STORIES[6]:
            raise AssertionError("No se preparo la historia original del mundo.")
        game._update_story(1.0)
        if not 0 < game.story_revealed_chars < len(game.story_text):
            raise AssertionError("El texto de la historia no se revelo gradualmente.")
        game._draw()
        if (
            game.screen.get_at((8, 8))[:3] != (0, 0, 0)
            or game.display.get_at((0, 0))[:3] != (0, 0, 0)
        ):
            raise AssertionError("La pantalla narrativa no tiene fondo negro.")
        story_pixels = pygame.surfarray.array3d(game.screen)[100:860, 180:550]
        if not np.any(
            (story_pixels[:, :, 0] > 150)
            & (story_pixels[:, :, 1] < 100)
            & (story_pixels[:, :, 2] < 100)
        ):
            raise AssertionError("La crónica del nivel no aparece en rojo.")
        game._handle_event(
            pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN})
        )
        if game.story_revealed_chars != len(game.story_text) or game.level != 7:
            raise AssertionError("ENTER no revelo la historia completa.")
        game._handle_event(
            pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN})
        )
        if game.level != 8 or game.lives != 3:
            raise AssertionError("El nuevo nivel no restauro las tres vidas.")

        game._start_level(1, reset_score=True)
        game.enemies.clear()
        game._start_boss()
        game._update_boss_intro(2.0)
        if game.state != "playing" or game.boss is None:
            raise AssertionError("El jefe no comenzo a luchar despues de su entrada.")
        initial_freeze_health = game.boss["health"]
        game._update_playing(
            0,
            pygame.key.get_pressed(),
            HandInput(freeze_active=True),
        )
        if (
            game.boss["health"] != initial_freeze_health - 15
            or game.boss["stun_timer"] <= 0
        ):
            raise AssertionError("El hielo no daño ni aturdio al jefe.")
        game._update_playing(
            0,
            pygame.key.get_pressed(),
            HandInput(freeze_active=True),
        )
        if game.boss["health"] != initial_freeze_health - 15:
            raise AssertionError("El hielo daño repetidamente mientras se mantenia.")
        initial_health = game.boss["health"]
        boss_x = game.boss["rect"].x
        game._update_boss(0.5, frozen=True)
        if game.boss["rect"].x != boss_x:
            raise AssertionError("El gesto de congelamiento no detuvo al jefe.")
        game._activate_poseidon()
        if game.boss["health"] != initial_health - 85 or game.boss["stun_timer"] <= 0:
            raise AssertionError("Las olas de Poseidon no danaron y aturdieron al jefe.")
        boss_x = game.boss["rect"].x
        game._update_boss(0.2, frozen=False)
        if game.boss["rect"].x != boss_x:
            raise AssertionError("El aturdimiento de Poseidon no detuvo al jefe.")
        game._activate_ares()
        if game.boss["health"] != initial_health - 160:
            raise AssertionError("El fuego de Ares no dano al jefe.")
        game._update_boss(0.1, frozen=False)
        if game.boss["health"] != initial_health - 169:
            raise AssertionError("El fuego de Ares no continuo quemando al jefe.")
        game._fire_ray_volley()
        if game.boss["health"] != initial_health - 214:
            raise AssertionError("El poder de energia no dano al jefe.")
        game._fire_ray_volley()
        if game.boss["health"] != initial_health - 214:
            raise AssertionError("El enfriamiento de energia no se aplico.")
        game._activate_zeus()
        if game.state != "level_complete" or game.boss["health"] != 0:
            raise AssertionError("El rayo de Zeus no termino el combate.")
        game.lives = 1
        game._reveal_story()
        game._handle_event(
            pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN})
        )
        if game.level != 2 or game.lives != 3:
            raise AssertionError("No se paso al segundo mundo con vida renovada.")

        for level in range(2, 11):
            expected_enemies = LEVEL_FORMATIONS[level - 1][0] * LEVEL_FORMATIONS[level - 1][1]
            if (
                game.level != level
                or game.wave_sizes[0] >= game.wave_sizes[1]
                or game.wave_sizes[1] >= game.wave_sizes[2]
                or game.wave_sizes[2] != expected_enemies
                or len(game.enemies) != game.wave_sizes[0]
                or game.lives != 3
                or game.level_boss_name != LEVEL_BOSS_NAMES[level - 1]
            ):
                raise AssertionError(f"El nivel {level} no tiene su mundo configurado.")
            if level == 10 and (
                {enemy["variant"] for enemy in game.enemies} != {0, 1}
                or LEVEL_BACKGROUND_FILES[9]
                != ("ares_portal.png", "ares_lava_world.png")
                or LEVEL_BOSS_SPRITE_FILES[9] != "ares_final_boss.png"
            ):
                raise AssertionError("El nivel 10 no usa todos los recursos del mundo de Ares.")
            game.lives = 1
            for expected_wave_count in game.wave_sizes[1:]:
                game.enemies.clear()
                game._update_enemies(0)
                if (
                    len(game.enemies) != expected_wave_count
                    or game.boss is not None
                ):
                    raise AssertionError(
                        f"El nivel {level} no avanzó correctamente sus oleadas."
                    )
            game.enemies.clear()
            game._update_enemies(0)
            if game.boss is None or game.state != "boss_intro":
                raise AssertionError(f"El nivel {level} no presento a su jefe.")
            boss_right_limit = WIDTH - 115 - game.boss["rect"].width
            game.boss["rect"].x = boss_right_limit - 1
            game.boss["direction"] = 1
            game.boss["shot_timer"] = 0.01
            bullets_before_boss_attack = len(game.bullets)
            game._update_boss(0.05, frozen=False)
            if (
                game.boss["rect"].right != WIDTH - 115
                or game.boss["direction"] != -1
                or len(game.bullets) <= bullets_before_boss_attack
            ):
                raise AssertionError(
                    f"El jefe del nivel {level} se salio del limite o no ataco."
                )
            if level == 10:
                game._damage_boss(180)
                game._update_boss(0, frozen=False)
                if game.boss["music_phase"] != 1:
                    raise AssertionError("La musica no cambio en la segunda fase final.")
                game._damage_boss(170)
                game._update_boss(0, frozen=False)
                if game.boss["music_phase"] != 2:
                    raise AssertionError("La musica no cambio en la fase final.")
                game._damage_boss(game.boss["health"])
                if (
                    game.state != "victory_intro"
                    or game.victory_intro_timer != VICTORY_INTRO_SECONDS
                    or "victory" not in game.audio.music_paths
                    or game.victory_image.get_size() != (WIDTH, HEIGHT)
                ):
                    raise AssertionError("No se inicio la presentación final con arte y música.")
                game._update_victory_intro(VICTORY_INTRO_SECONDS)
                if game.state != "victory":
                    raise AssertionError("La espera no mostro el mensaje de victoria.")
                game.state = "victory_intro"
                game.victory_intro_timer = VICTORY_INTRO_SECONDS
                game._handle_event(
                    pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN})
                )
                if game.state != "victory":
                    raise AssertionError("ENTER no mostro el mensaje de victoria.")
                game._draw()
            else:
                game._damage_boss(game.boss["max_health"])
                if game.state != "level_complete":
                    raise AssertionError(f"El jefe del nivel {level} no fue derrotado.")
                game._reveal_story()
                game._handle_event(
                    pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN})
                )
                if game.lives != 3:
                    raise AssertionError("El siguiente nivel no recupero todas las vidas.")
        game._draw()
        print(
            "Prueba correcta: recursos, ventana, historia, diez mundos, salud, "
            "gestos, efectos y sonidos."
        )
    finally:
        game.close()


def main() -> None:
    """Inicia las pruebas sin ventana real o arranca el juego normal."""
    if "--self-test" in sys.argv:
        import os

        os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
        os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
        self_test()
        return
    Game().run()


if __name__ == "__main__":
    main()
