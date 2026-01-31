def structure_visual_conversation(blocks, image_width):
    midpoint = image_width / 2
    messages = []

    for b in blocks:
        speaker = "Person_A" if b["x"] < midpoint else "Person_B"
        messages.append({
            "speaker": speaker,
            "message": b["text"],
            "y": b["y"]
        })

    # sort top → bottom
    messages.sort(key=lambda m: m["y"])

    return messages
