import requests
import random
import re
from nicegui import ui

api_url = "https://api.dictionaryapi.dev/api/v2/entries/en/<word>"
albums = {}  # Dictionary để lưu trữ các album flashcard
topic_flashcards = {
    "Nghề nghiệp": [
        {"word": "chef (n)", "info": "đầu bếp"},
        {"word": "comedian (n)", "info": "diễn viên hài"},
        {"word": "delivery man (n)", "info": "nhân viên giao hàng"},
        {"word": "doctor (n)", "info": "bác sĩ"},
        {"word": "entrepreneur (n)", "info": "nhà kinh doanh"},
        {"word": "engineer (n)", "info": "kỹ sư"},
        {"word": "factory worker (n)", "info": "công nhân nhà máy"},
        {"word": "office worker (n)", "info": "nhân viên văn phòng"},
        {"word": "florist (n)", "info": "người bán hoa"},
        {"word": "hairdresser (n)", "info": "thợ cắt tóc"},
    ],
    "Trái cây": [
        {"word": "pear (n)", "info": "quả lê"},
        {"word": "grape (n)", "info": "quả nho"},
        {"word": "peach (n)", "info": "quả đào"},
        {"word": "orange (n)", "info": "quả cam"},
        {"word": "mango (n)", "info": "quả xoài"},
        {"word": "coconut (n)", "info": "quả dừa"},
        {"word": "pineapple (n)", "info": "quả dứa"},
        {"word": "watermelon (n)", "info": "dưa hấu"},
        {"word": "durian (n)", "info": "sầu riêng"},
        {"word": "lychee (n)", "info": "quả vải"},
        {"word": "guava (n)", "info": "quả ổi"},
        {"word": "starfruit (n)", "info": "quả khế"},
    ],
    "Gia đình": [
        {"word": "parent (n)", "info": "bố hoặc mẹ"},
        {"word": "daughter (n)", "info": "con gái"},
        {"word": "son (n)", "info": "con trai"},
        {"word": "sibling (n)", "info": "anh chị em ruột"},
        {"word": "sister (n)", "info": "chị, em gái"},
        {"word": "brother (n)", "info": "anh, em trai"},
        {"word": "grandmother (n)", "info": "bà nội (ngoại)"},
        {"word": "grandfather (n)", "info": "ông nội (ngoại)"},
        {"word": "grandparent (n)", "info": "ông hoặc bà"},
        {"word": "relative (n)", "info": "họ hàng"},
        {"word": "aunt (n)", "info": "cô, dì"},
        {"word": "uncle (n)", "info": "chú, bác, cậu, dượng"},
    ],
    "Động Vật": [
        {"word": "mouse (n)", "info": "con chuột"},
        {"word": "cat (n)", "info": "con mèo"},
        {"word": "dog (n)", "info": "con chó"},
        {"word": "kitten (n)", "info": "mèo con"},
        {"word": "puppy (n)", "info": "chó con"},
        {"word": "pig (n)", "info": "con lợn, heo"},
        {"word": "chicken (n)", "info": "con gà"},
        {"word": "duck (n)", "info": "con vịt"},
        {"word": "goose (n)", "info": "con ngỗng"},
        {"word": "turkey (n)", "info": "con gà tây"},
        {"word": "stork (n)", "info": "con cò"},
        {"word": "swan (n)", "info": "thiên nga"},
    ],
    "Rau Quả": [
        {"word": "bean (n)", "info": "hạt đậu"},
        {"word": "pea (n)", "info": "đậu Hà Lan"},
        {"word": "cabbage (n)", "info": "bắp cải"},
        {"word": "carrot (n)", "info": "củ cà rốt"},
        {"word": "corn (n)", "info": "ngô, bắp"},
        {"word": "cucumber (n)", "info": "dưa chuột"},
        {"word": "tomato (n)", "info": "quả cà chua"},
        {"word": "garlic (n)", "info": "tỏi"},
        {"word": "onion (n)", "info": "củ hành"},
        {"word": "spring onion (n)", "info": "hành lá"},
        {"word": "ginger (n)", "info": "củ gừng"},
        {"word": "turmeric (n)", "info": "củ nghệ"},
        {"word": "potato (n)", "info": "khoai tây"},
        {"word": "sweet potato (n)", "info": "khoai lang"},
    ],
    "Đồ Ăn": [
        {"word": "soup (n)", "info": "món súp, món canh"},
        {"word": "salad (n)", "info": "rau trộn, nộm rau"},
        {"word": "bread (n)", "info": "bánh mì"},
        {"word": "sausage (n)", "info": "xúc xích"},
        {"word": "hot dog (n)", "info": "bánh mỳ kẹp xúc xích"},
        {"word": "bacon (n)", "info": "thịt xông khói"},
        {"word": "ham (n)", "info": "thịt giăm bông"},
        {"word": "egg (n)", "info": "trứng"},
        {"word": "pork (n)", "info": "thịt lợn"},
        {"word": "beef (n)", "info": "thịt bò"},
        {"word": "chicken (n)", "info": "thịt gà"},
        {"word": "duck (n)", "info": "thịt vịt"},
        {"word": "lamb (n)", "info": "thịt cừu"},
        {"word": "ribs (n)", "info": "sườn"},
    ],
    "Động tác cơ thể": [
        {"word": "tiptoe (v)", "info": "đi nhón chân"},
        {"word": "jump (v)", "info": "nhảy"},
        {"word": "leap (v)", "info": "nhảy vọt, nhảy xa"},
        {"word": "stand (v)", "info": "đứng"},
        {"word": "sit (v)", "info": "ngồi"},
        {"word": "lean (v)", "info": "dựa, tựa"},
        {"word": "wave (v)", "info": "vẫy tay"},
        {"word": "clap (v)", "info": "vỗ tay"},
        {"word": "point (v)", "info": "chỉ, trỏ"},
        {"word": "catch (v)", "info": "bắt, đỡ"},
        {"word": "stretch (v)", "info": "vươn (vai..), ưỡn lưng"},
        {"word": "push (v)", "info": "đẩy"},
        {"word": "pull (v)", "info": "kéo"},
        {"word": "crawl (v)", "info": "bò, trườn"},
    ],
    'Bộ phận cơ thế': [
    {"word": "head (n)", "info": "đầu"},
    {"word": "hair (n)", "info": "tóc"},
    {"word": "face (n)", "info": "gương mặt"},
    {"word": "forehead (n)", "info": "trán"},
    {"word": "eyebrow (n)", "info": "lông mày"},
    {"word": "eye (n)", "info": "mắt"},
    {"word": "eyelash (n)", "info": "lông mi"},
    {"word": "nose (n)", "info": "mũi"},
    {"word": "ear (n)", "info": "tai"},
    {"word": "cheek (n)", "info": "má"} 
    ],
    'Trường học': [
    {"word": "school (n)", "info": "trường học"},
    {"word": "class (n)", "info": "lớp học"},
    {"word": "student (n)", "info": "học sinh, sinh viên"},
    {"word": "pupil (n)", "info": "học sinh"},
    {"word": "teacher (n)", "info": "giáo viên"},
    {"word": "principal (n)", "info": "hiệu trưởng"},
    {"word": "course (n)", "info": "khóa học"},
    {"word": "semester (n)", "info": "học kì"},
    {"word": "exercise (n)", "info": "bài tập"},
    {"word": "homework (n)", "info": "bài tập về nhà"}
    ],
    'Tính cách': [
    {"word": "active (adj)", "info": "năng nổ, lanh lợi"},
    {"word": "alert (adj)", "info": "tỉnh táo, cảnh giác"},
    {"word": "ambitious (adj)", "info": "tham vọng"},
    {"word": "attentive (adj)", "info": "chăm chú, chú tâm"},
    {"word": "bold (adj)", "info": "táo bạo, mạo hiểm"},
    {"word": "brave (adj)", "info": "dũng cảm, gan dạ"},
    {"word": "careful (adj)", "info": "cẩn thận, thận trọng"},
    {"word": "careless (adj)", "info": "bất cẩn, cẩu thả"},
    {"word": "cautious (adj)", "info": "thận trọng, cẩn thận"},
    {"word": "conscientious (adj)", "info": "chu đáo, tỉ mỉ"},
    {"word": "courageous (adj)", "info": "can đảm"}
    ],
    'Đồ dùng học tập': 
    [
    {"word": "pen (n)", "info": "bút mực"},
    {"word": "pencil (n)", "info": "bút chì"},
    {"word": "highlighter (n)", "info": "bút nhớ"},
    {"word": "ruler (n)", "info": "thước kẻ"},
    {"word": "eraser (n)", "info": "tẩy, gôm"},
    {"word": "pencil case (n)", "info": "hộp bút"},
    {"word": "book (n)", "info": "quyển sách"},
    {"word": "notebook (n)", "info": "vở"},
    {"word": "paper (n)", "info": "giấy"},
    {"word": "scissors (n)", "info": "kéo"}
     ],
    'Thiên nhiên ': [
    {"word": "forest (n)", "info": "rừng"},
    {"word": "rainforest (n)", "info": "rừng mưa nhiệt đới"},
    {"word": "mountain (n)", "info": "núi, dãy núi"},
    {"word": "highland (n)", "info": "cao nguyên"},
    {"word": "hill (n)", "info": "đồi"},
    {"word": "valley (n)", "info": "thung lũng, châu thổ, lưu vực"},
    {"word": "cave (n)", "info": "hang động"},
    {"word": "rock (n)", "info": "đá"},
    {"word": "slope (n)", "info": "dốc"},
    {"word": "volcano (n)", "info": "núi lửa"}
    ],
    'Du lịch': [
    {"word": "travel (v)", "info": "đi du lịch"},
    {"word": "depart (v)", "info": "khởi hành"},
    {"word": "leave (v)", "info": "rời đi"},
    {"word": "arrive (v)", "info": "đến nơi"},
    {"word": "airport (n)", "info": "sân bay"},
    {"word": "take off (v)", "info": "cất cánh"},
    {"word": "land (v)", "info": "hạ cánh"},
    {"word": "check in (v)", "info": "đăng ký phòng ở khách sạn"},
    {"word": "check out (v)", "info": "trả phòng khách sạn"},
    {"word": "visit (v)", "info": "thăm viếng"}
]
}

def get_word_info(word):
    result = requests.get(api_url.replace("<word>", word))
    return result.json()

def search_word():
    word = input_word.value
    if not word:
        output.set_text("Vui lòng nhập một từ.")
        return
    
    try:
        data = get_word_info(word)
        if isinstance(data, list) and len(data) > 0:
            word_data = data[0]
            phonetic = word_data.get('phonetic', 'Không có phát âm')
            meanings = word_data.get('meanings', [])
            
            output_text = f"Từ: {word}\nPhát âm: {phonetic}\n\n"
            
            for meaning in meanings:
                part_of_speech = meaning.get('partOfSpeech', '')
                definitions = meaning.get('definitions', [])
                if definitions:
                    output_text += f"{part_of_speech.capitalize()}:\n"
                    for i, definition in enumerate(definitions, 1):
                        output_text += f"{i}. {definition.get('definition', '')}\n"
                    output_text += "\n"
            
            output.set_text(output_text)
            add_to_flashcard_button.enable()
        else:
            output.set_text(f"Không tìm thấy thông tin cho từ '{word}'.")
            add_to_flashcard_button.disable()
    except Exception as e:
        output.set_text(f"Có lỗi xảy ra: {str(e)}")
        add_to_flashcard_button.disable()

def add_to_flashcard():
    word = input_word.value
    info = output.text
    album_name = album_select.value
    if not album_name:
        ui.notify("Vui lòng chọn một album trước khi thêm từ", color="warning")
        return
    if album_name not in albums:
        albums[album_name] = []
    albums[album_name].append({"word": word, "info": info})
    ui.notify(f"Đã thêm '{word}' vào album '{album_name}'")
    if word_scramble_game:
        word_scramble_game.update_album_options()

def create_album():
    new_album_name = new_album_input.value
    if new_album_name and new_album_name not in albums:
        albums[new_album_name] = []
        update_album_select()
        album_select.value = new_album_name
        new_album_input.value = ""
        ui.notify(f"Đã tạo album mới: {new_album_name}")
        if word_scramble_game:
            word_scramble_game.update_album_options()
    elif new_album_name in albums:
        ui.notify("Album đã tồn tại", color="warning")
    else:
        ui.notify("Vui lòng nhập tên album", color="warning")

def update_album_select():
    album_select.options = list(albums.keys())
    album_select.update()
    study_album_select.options = list(albums.keys())
    study_album_select.update()

class ReviewMistakes:
    def __init__(self, container):
        self.container = container
        self.mistake_words = []  # Lưu các từ làm sai
        self.current_review_word = None
        self.setup_ui()
    
    def setup_ui(self):
        with self.container:
            ui.label("Ôn tập từ vựng sai").classes('text-2xl font-bold mb-4')
            
            # Hiển thị số lượng từ cần ôn tập
            self.count_label = ui.label().classes('mb-4')
            self.update_count_label()
            
            # Giao diện ôn tập
            self.review_interface = ui.column().classes('w-full')
            with self.review_interface:
                self.word_display = ui.label().classes('text-xl mb-4')
                with ui.row().classes('gap-2 mb-4'):
                    self.reveal_button = ui.button(
                        "Hiện từ", 
                        on_click=self.reveal_word
                    ).classes('bg-blue-500')
                    self.known_button = ui.button(
                        "Đã thuộc", 
                        on_click=self.mark_as_known
                    ).classes('bg-green-500')
                    self.unknown_button = ui.button(
                        "Chưa thuộc", 
                        on_click=self.mark_as_unknown
                    ).classes('bg-red-500')
            
            # Ban đầu ẩn giao diện ôn tập
            self.review_interface.set_visibility(False)
            
            # Nút bắt đầu ôn tập
            self.start_review_button = ui.button(
                "Bắt đầu ôn tập", 
                on_click=self.start_review
            ).classes('bg-purple-500 mb-4')
    
    def add_mistake(self, word):
        if word not in self.mistake_words:
            self.mistake_words.append(word)
            self.update_count_label()
    
    def update_count_label(self):
        self.count_label.set_text(f"Số từ cần ôn tập: {len(self.mistake_words)}")
    
    def start_review(self):
        if not self.mistake_words:
            ui.notify("Không có từ nào cần ôn tập!", color="warning")
            return
        
        self.review_interface.set_visibility(True)
        self.start_review_button.set_visibility(False)
        self.next_review_word()
    
    def next_review_word(self):
        if not self.mistake_words:
            ui.notify("Đã ôn tập xong tất cả các từ!", color="success")
            self.review_interface.set_visibility(False)
            self.start_review_button.set_visibility(True)
            return
        
        self.current_review_word = random.choice(self.mistake_words)
        self.word_display.set_text("Hãy nhớ lại từ này: ???")
        self.reveal_button.set_visibility(True)
        self.known_button.set_visibility(False)
        self.unknown_button.set_visibility(False)
    
    def reveal_word(self):
        self.word_display.set_text(f"Từ: {self.current_review_word}")
        self.reveal_button.set_visibility(False)
        self.known_button.set_visibility(True)
        self.unknown_button.set_visibility(True)
    
    def mark_as_known(self):
        self.mistake_words.remove(self.current_review_word)
        self.update_count_label()
        ui.notify(f"Đã đánh dấu '{self.current_review_word}' là đã thuộc", color="success")
        self.next_review_word()
    
    def mark_as_unknown(self):
        ui.notify(f"Tiếp tục ôn tập '{self.current_review_word}'", color="warning")
        self.next_review_word()

class WordScrambleGame:
    def __init__(self, container):
        self.container = container
        self.current_word = ""
        self.scrambled_word = ""
        self.score = 0
        self.filtered_words = []
        self.game_mode = None
        self.is_game_active = False
        self.mistake_reviewer = None  # Sẽ được khởi tạo sau
        self.setup_ui()
    
    def get_filtered_words(topic):
        return [re.sub(r'\s\(.*\)', '', entry["word"]) for entry in topic_flashcards[topic]]

    def update_album_options(self):
   
        if hasattr(self, 'source_select') and self.game_mode == 'album':
            current_value = self.source_select.value
            self.source_select.options = list(albums.keys())
            self.source_select.value = current_value
        
        # Nếu đang trong chế độ album, cập nhật lại danh sách từ
        if self.is_game_active and current_value in albums:
            self.filtered_words = [entry["word"] for entry in albums[current_value]]
    def setup_ui(self):
        with self.container:
            # Game interface
            with ui.tabs().classes('w-full') as tabs:
                play_tab = ui.tab('Chơi game')
                review_tab = ui.tab('Ôn tập')
            
            with ui.tab_panels(tabs).classes('w-full'):
                # Panel chơi game
                with ui.tab_panel(play_tab):
                    ui.label("Trò Chơi Sắp Xếp Lại Từ").classes('text-3xl font-bold mb-4')
                    
                    with ui.row().classes('gap-4 mb-4'):
                        ui.button("Album của tôi", on_click=lambda: self.show_mode_options('album')).classes('bg-blue-500')
                        ui.button("Chủ đề có sẵn", on_click=lambda: self.show_mode_options('topic')).classes('bg-green-500')
                    
                    self.mode_container = ui.column().classes('w-full mb-4')
                    self.game_controls = ui.column().classes('w-full mb-4')
                    
                    with self.game_controls:
                        self.start_button = ui.button(
                            "Bắt đầu trò chơi", 
                            on_click=self.start_new_game
                        ).classes('bg-green-500 mb-4')
                        self.reset_button = ui.button(
                            "Chơi lại", 
                            on_click=self.reset_game
                        ).classes('bg-yellow-500 mb-4')
                    
                    self.game_interface = ui.column().classes('w-full')
                    with self.game_interface:
                        self.score_label = ui.label(f"Điểm: {self.score}").classes('text-lg mb-4')
                        self.word_display = ui.label().classes('text-xl mb-4')
                        self.hint_label = ui.label().classes('text-sm text-gray-500 mb-4')
                        
                        with ui.row().classes('gap-2'):
                            self.input_box = ui.input(placeholder='Nhập từ của bạn...').classes('w-64')
                            self.check_button = ui.button(
                                "Kiểm tra", 
                                on_click=self.check_word
                            ).classes('bg-blue-500')
                            self.skip_button = ui.button(
                                "Bỏ qua", 
                                on_click=self.skip_word
                            ).classes('bg-gray-500')
                
                # Panel ôn tập
                with ui.tab_panel(review_tab):
                    self.mistake_reviewer = ReviewMistakes(ui.column().classes('w-full'))
            
            # Initially hide game controls and interface
            self.game_controls.set_visibility(False)
            self.game_interface.set_visibility(False)
    
    
    def show_mode_options(self, mode):
        self.game_mode = mode
        self.mode_container.clear()
        self.game_controls.set_visibility(False)
        self.game_interface.set_visibility(False)
        self.is_game_active = False
        
        with self.mode_container:
            if mode == 'album':
                if not albums:
                    ui.label("Bạn chưa có album nào. Hãy tạo album trong phần Từ điển.").classes('text-red-500')
                    return
                
                self.source_select = ui.select(
                    label="Chọn album",
                    options=list(albums.keys()),
                    on_change=self.on_source_change
                ).classes('w-full max-w-xs mb-4')
            else:  # mode == 'topic'
                self.source_select = ui.select(
                    label="Chọn chủ đề",
                    options=list(topic_flashcards.keys()),
                    on_change=self.on_source_change
                ).classes('w-full max-w-xs mb-4')
    
    def on_source_change(self):
        selected_source = self.source_select.value
        if not selected_source:
            return
    
    # Get words based on selected mode and source
        if self.game_mode == 'album':
         self.filtered_words = [entry["word"] for entry in albums[selected_source]]
        else:  # topic mode
            self.filtered_words = [entry["word"] for entry in topic_flashcards[selected_source]]
    
        if not self.filtered_words:
            ui.notify("Không có từ nào trong nguồn này", color="warning")
            return
    
    # Reset game state
        self.is_game_active = False
        self.score = 0
        self.score_label.set_text(f"Điểm: {self.score}")
        self.word_display.set_text("")
        self.hint_label.set_text("")
        self.input_box.value = ""
    
    # Show game controls but not game interface yet
        self.game_controls.set_visibility(True)
        self.start_button.set_visibility(True)
        self.reset_button.set_visibility(False)
    def start_new_game(self):
        selected_source = self.source_select.value
        if self.game_mode == 'album':
            self.filtered_words = [entry["word"] for entry in albums[selected_source]]
        else:  # topic mode
            self.filtered_words = [entry["word"] for entry in topic_flashcards[selected_source]]
    
        if not self.filtered_words:
            ui.notify("Vui lòng chọn một nguồn từ vựng trước.", color="warning")
            return
    
        self.is_game_active = True
        self.score = 0
        self.score_label.set_text(f"Điểm: {self.score}")
        self.game_interface.set_visibility(True)
        self.start_button.set_visibility(False)
        self.reset_button.set_visibility(True)
        self.input_box.value = ""
        self.next_word()
    
    def reset_game(self):
    # Reset game state
        self.is_game_active = False
        self.score = 0
        self.score_label.set_text(f"Điểm: {self.score}")
        self.word_display.set_text("")
        self.hint_label.set_text("")
        self.input_box.value = ""
    
    # Restart game
        self.start_new_game()
        
    def next_word(self):
        if not self.is_game_active:
            return
            
        self.current_word = random.choice(self.filtered_words)
        self.scrambled_word = ''.join(random.sample(self.current_word, len(self.current_word)))
        
        # Make sure scrambled word is different from original
        while self.scrambled_word == self.current_word and len(self.current_word) > 1:
            self.scrambled_word = ''.join(random.sample(self.current_word, len(self.current_word)))
            
        self.word_display.set_text(f"Từ đã xáo trộn: {self.scrambled_word}")
        self.hint_label.set_text(f"Độ dài từ: {len(self.current_word)} chữ cái")
        self.input_box.value = ""
    
    def skip_word(self):
        if not self.is_game_active:
            return
            
        ui.notify(f"Từ đúng là: {self.current_word}", color="warning")
        self.next_word()
    
    def check_word(self):
        if not self.is_game_active:
            return
            
        user_input = self.input_box.value.strip().lower()
        if not user_input:
            ui.notify("Vui lòng nhập từ cần kiểm tra", color="warning")
            return
        
        if user_input == self.current_word.lower():
            self.score += 1
            ui.notify("Chính xác! +1 điểm", color="success")
        else:
            ui.notify(f"Sai rồi! Từ đúng là: {self.current_word}", color="error")
            # Thêm từ vào danh sách ôn tập khi làm sai
            self.mistake_reviewer.add_mistake(self.current_word)
        
        self.score_label.set_text(f"Điểm: {self.score}")
        self.next_word()
def show_flashcards():
    study_container.clear()
    
    album_name = study_album_select.value
    if not album_name or album_name not in albums or not albums[album_name]:
        ui.notify("Vui lòng chọn một album có từ vựng", color="warning")
        return

    flashcards = albums[album_name]
    
    with study_container:
        ui.label("Flip Flashcards").classes('text-xl font-bold mb-4')
        with ui.row().classes('flex flex-wrap gap-4 mb-8'):
            for card in flashcards:
                create_flashcard(card['word'], card['info'])

def create_flashcard(word, info):
    def flip_card():
        if card_content.text == word:
            card_content.set_text(info)
        else:
            card_content.set_text(word)

    with ui.card().classes('w-80 h-48 m-2 cursor-pointer overflow-auto').on('click', flip_card):
        card_content = ui.label(word).classes('text-center text-lg font-bold h-full flex items-center justify-center')

def show_topic_flashcards():
    topic_container.clear()
    
    with topic_container:
        ui.label("Chủ đề từ vựng").classes('text-xl font-bold mb-4')
        with ui.row().classes('flex flex-wrap gap-4 mb-8'):
            for topic in topic_flashcards:
                topic_btn = ui.button(topic, on_click=lambda t=topic: study_topic_flashcards(t))
                topic_btn.classes('w-48 h-20 bg-blue-500 text-white font-bold rounded')

def study_topic_flashcards(topic):
    study_container.clear()
    
    with study_container:
        ui.label(f"Từ vựng chủ đề: {topic}").classes('text-xl font-bold mb-4')
        for card in topic_flashcards[topic]:
            create_flashcard(card['word'], card['info'])

# Tạo giao diện chính với các tab
with ui.tabs() as tabs:
    dictionary_tab = ui.tab('Từ điển')
    flashcard_tab = ui.tab('Flashcards')
    game_tab = ui.tab('Trò chơi')

with ui.tab_panels(tabs, value=dictionary_tab).classes('w-full'):
    with ui.tab_panel(dictionary_tab):
        with ui.column():
            ui.label("Tra cứu từ điển tiếng Anh")
            with ui.row():
                input_word = ui.input(label="Nhập từ cần tra cứu")
                ui.button("Tìm kiếm", on_click=search_word)
            output = ui.label().classes('whitespace-pre-wrap')
            
            with ui.row():
                new_album_input = ui.input(label="Tên album mới")
                ui.button("Tạo album", on_click=create_album)
            
            with ui.row():
                album_select = ui.select(label="Chọn album", options=[])
                add_to_flashcard_button = ui.button("Thêm vào Flashcard", on_click=add_to_flashcard)
                add_to_flashcard_button.disable()

    with ui.tab_panel(flashcard_tab):
        with ui.column():
            ui.label("Học Flashcards").classes('text-xl font-bold mb-4')
            with ui.row():
                study_album_select = ui.select(label="Chọn album để học", options=[])
                topic_container = ui.column().classes('w-full')
                ui.button("Xem Flashcards", on_click=show_flashcards)
                ui.button("Xem chủ đề từ vựng", on_click=show_topic_flashcards)
            study_container = ui.column().classes('w-full')

    with ui.tab_panel(game_tab):
        game_container = ui.column().classes('w-full p-4')
        word_scramble_game = WordScrambleGame(game_container)

ui.run()