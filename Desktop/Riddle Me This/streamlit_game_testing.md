**Streamlit Game Testing & Troubleshooting Guide**

---

### ✅ **Run and Test Locally First**

Before deploying to Streamlit Cloud, confirm everything works locally:

1. Open your terminal and navigate to your project folder:

   ```bash
   cd my-streamlit-game
   ```

2. Run the app:

   ```bash
   streamlit run app.py
   ```

3. Your browser will open to `http://localhost:8501`. Interact with your app to verify:

   - Text displays properly
   - Buttons, inputs, or spelling game features respond correctly
   - Any media (images, sounds) load without errors

---

### 🧪 **Checklist for Game Testing**

-

---

### 🧰 **Debugging Common Issues**

#### ❌ Streamlit doesn't launch or shows error

- Check for syntax errors
- Run: `python app.py` to confirm the script itself is clean
- Check you're in the correct folder (`ls` to list files)

#### 📦 Missing a module

```bash
ModuleNotFoundError: No module named 'xyz'
```

- Install it: `pip install xyz`
- Add it to `requirements.txt`

#### 📁 File not found

```bash
FileNotFoundError: [Errno 2] No such file or directory: 'data/words.json'
```

- Make sure the file exists in your project folder
- Use relative paths like `open("data/words.json")`

#### 🖼️ Images not showing

- Check image path (e.g., `st.image("images/logo.png")`)
- Make sure the file is committed and pushed to GitHub

---

### 🛰️ **After Deployment**

Once deployed on Streamlit Cloud:

1. Test the app link provided by Streamlit
2. Confirm everything works just like it did locally
3. If there's an error, click the **"View logs"** button in Streamlit Cloud for detailed error messages

---

Let me know what features your game includes (buttons, sound, scoring, etc.), and I can update this guide with more specific checks!

