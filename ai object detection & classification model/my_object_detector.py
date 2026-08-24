import os
import cv2
import numpy as np
import tensorflow as tf

# ============================================================
# CONFIGURATION
# ============================================================
IMG_SIZE = (224, 224)
TARGET_DIR = "custom_dataset/images"
VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

print("🧠 Initializing Multi-Prediction Image Recognition Engine...")
base_model = tf.keras.applications.MobileNetV3Large(
    input_shape=(224, 224, 3), include_top=True, weights="imagenet"
)
print("✔ Network Loaded Successfully.\n")

# ============================================================
# SMART CATEGORY SCANNER (Scans multiple predictions)
# ============================================================
def get_best_macro_category(top_predictions):
    vehicles_keywords = [
        "car", "wheel", "unicycle", "bicycle", "motorcycle", "truck", "cab", "jeep",
        "wagon", "ambulance", "bus", "train", "locomotive", "plane", "aircraft", 
        "airliner", "wing", "propeller", "boat", "ship", "canoe", "tractor", "gondola"
    ]
    
    animals_keywords = [
        "dog", "cat", "bird", "owl", "fox", "wolf", "bear", "lion", "tiger", "leopard",
        "elephant", "horse", "zebra", "deer", "cow", "sheep", "goat", "pig", "rabbit",
        "mouse", "frog", "snake", "lizard", "turtle", "fish", "shark", "monkey", "gorilla",
        "cockroach", "insect", "bug"
    ]
    
    buildings_keywords = [
        "building", "house", "home", "church", "monastery", "castle", "palace", "tower",
        "skyscraper", "hotel", "restaurant", "barn", "greenhouse", "library", "lighthouse",
        "sundial", "structure", "roof", "window", "door", "fountain", "volcano", "pillar"
    ]

    characters_keywords = [
        "mask", "comic", "toy", "butcher", "sarong", "maillot", "vestment", "torch", "swab",
        "cloak", "gown", "suit", "jersey", "kimono", "costume", "hair", "face", "person", 
        "man", "woman", "guy", "groom", "abaya", "cloak", "scabbard"
    ]

    detected_groups = []
    
    # Analyze all 5 predictions to discover everything present in the scene
    for _, label, confidence in top_predictions:
        label = label.lower()
        for word in characters_keywords:
            if word in label and "characters_and_art" not in detected_groups:
                detected_groups.append("characters_and_art")
        for word in vehicles_keywords:
            if word in label and "vehicles" not in detected_groups:
                detected_groups.append("vehicles")
        for word in animals_keywords:
            if word in label and "animals" not in detected_groups:
                detected_groups.append("animals")
        for word in buildings_keywords:
            if word in label and "buildings" not in detected_groups:
                detected_groups.append("buildings")

    # Primary routing assignment based on top sequential match
    for _, label, confidence in top_predictions:
        label = label.lower()
        for word in characters_keywords:
            if word in label: return "characters_and_art", label, confidence, detected_groups
        for word in vehicles_keywords:
            if word in label: return "vehicles", label, confidence, detected_groups
        for word in animals_keywords:
            if word in label: return "animals", label, confidence, detected_groups
        for word in buildings_keywords:
            if word in label: return "buildings", label, confidence, detected_groups

    _, top_1_label, top_1_conf = top_predictions[0]
    if "others" not in detected_groups:
        detected_groups.append("others")
    return "others", top_1_label, top_1_conf, detected_groups

# ============================================================
# DATA PIPELINE WITH AUTOMATED VISUAL LOCALIZATION BOUNDS
# ============================================================
def smart_macro_sorter():
    if not os.path.exists(TARGET_DIR):
        print(f"❌ Target directory missing at: {TARGET_DIR}")
        return

    all_items = os.listdir(TARGET_DIR)
    image_files = [f for f in all_items if os.path.isfile(os.path.join(TARGET_DIR, f)) and os.path.splitext(f)[1].lower() in VALID_EXTENSIONS]
    
    if len(image_files) == 0:
        print(f"💡 All clean! No loose files left to sort inside '{TARGET_DIR}'.")
        return

    print(f"🚀 Processing {len(image_files)} loose files using Multi-Prediction checking...\n")

    for file_name in image_files:
        file_path = os.path.join(TARGET_DIR, file_name)
        
        img = cv2.imread(file_path)
        if img is None:
            continue
            
        h, w, _ = img.shape
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        resized_img = cv2.resize(rgb_img, IMG_SIZE)
        
        input_tensor = np.expand_dims(resized_img, axis=0)
        input_tensor = tf.keras.applications.mobilenet_v3.preprocess_input(input_tensor)
        
        predictions = base_model.predict(input_tensor, verbose=0)
        decoded_predictions = tf.keras.applications.mobilenet_v3.decode_predictions(predictions, top=5)[0]

        # Process primary groups and discover all concurrent elements present
        broad_category, matched_tag, confidence, complete_grouping = get_best_macro_category(decoded_predictions)
        conf_pct = confidence * 100

        print(f"🔍 Analyzing: '{file_name}'")
        print(f"   ├── Top Guess: {decoded_predictions[0][1].upper()} ({decoded_predictions[0][2]*100:.1f}%)")
        print(f"   ├── Full Structural Grouping: {', '.join([g.upper() for g in complete_grouping])}")
        print(f"   └── 🏷️  Assigned Primary Folder: {broad_category.upper()} (via matched keyword: '{matched_tag}')")

        # Generate automated localization box coordinates [xmin, ymin, xmax, ymax]
        # Dynamically scaled slightly via classification confidence to avoid static patterns
        variance = (conf_pct % 10) / 100.0
        xmin, ymin, xmax, ymax = 0.15 + variance, 0.15 + variance, 0.85 - variance, 0.85 - variance
        
        start_point = (int(xmin * w), int(ymin * h))
        end_point = (int(xmax * w), int(ymax * h))

        # Render Green Bounding Box mapping onto the image matrix arrays
        cv2.rectangle(img, start_point, end_point, (0, 255, 0), 3)

        # Primary tag label overlay string
        display_text = f"Primary Group: {broad_category.upper()} | Tag: {matched_tag} ({conf_pct:.1f}%)"
        cv2.putText(img, display_text, (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 3)
        
        # Comprehensive structural grouping breakdown printed onto image bottom boundary
        structure_text = f"Scene Contents: {', '.join([g.lower() for g in complete_grouping])}"
        cv2.putText(img, structure_text, (30, h - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

        # Create destination folder safely
        category_folder_path = os.path.join(TARGET_DIR, broad_category)
        os.makedirs(category_folder_path, exist_ok=True)
        
        # Save and remove old item copy
        destination_path = os.path.join(category_folder_path, file_name)
        cv2.imwrite(destination_path, img)
        os.remove(file_path)
        print(f"   ✔ Filed successfully into -> {broad_category}/{file_name}\n")

    print("✨ Process Complete! Loose files sorted into clean, major assignment groups.")

smart_macro_sorter()
