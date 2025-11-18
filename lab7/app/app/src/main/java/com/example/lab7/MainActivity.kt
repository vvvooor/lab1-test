package com.example.lab7

import android.content.Context
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.datastore.preferences.preferencesDataStore
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.runBlocking
import kotlinx.serialization.decodeFromString
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import kotlinx.serialization.Serializable
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics

// DataStore
val Context.dataStore: DataStore<Preferences> by preferencesDataStore(name = "notes_prefs")

@Serializable
data class Note(val id: Int, var title: String, var content: String)

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Загружаем заметки из DataStore при старте
        val savedNotes = loadNotes(this)

        setContent {
            NotesApp(savedNotes)
        }
    }
}

// Ключ для хранения заметок
val NOTES_KEY = stringPreferencesKey("notes_key")

fun loadNotes(context: Context): MutableList<Note> = runBlocking {
    val json = context.dataStore.data.first()[NOTES_KEY] ?: "[]"
    Json.decodeFromString<List<Note>>(json)   //
}.toMutableList()

fun saveNotes(context: Context, notes: List<Note>) {
    runBlocking {
        context.dataStore.edit { prefs ->
            prefs[NOTES_KEY] = Json.encodeToString(notes)
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun NotesApp(initialNotes: MutableList<Note>) {
    var notes by remember { mutableStateOf(initialNotes) }
    var showDialog by remember { mutableStateOf(false) }
    var editNote by remember { mutableStateOf<Note?>(null) }

    val context = LocalContext.current

    Scaffold(
        topBar = { TopAppBar(title = { Text("Мои заметки") }) },
        floatingActionButton = {
            FloatingActionButton(onClick = { editNote = null; showDialog = true }, modifier = Modifier.semantics { contentDescription = "Add" }) {
                Text("+")

            }
        }
    ) { padding ->
        Box(modifier = Modifier.padding(padding)) {
            NotesList(
                notes = notes,
                onEdit = { note ->
                    editNote = note
                    showDialog = true
                },
                onDelete = { note ->
                    notes.remove(note)
                    saveNotes(context, notes)
                }
            )

            if (showDialog) {
                AddEditNoteDialog(
                    note = editNote,
                    onDismiss = { showDialog = false },
                    onSave = { title, content ->
                        if (editNote == null) {
                            val id = if (notes.isEmpty()) 1 else notes.maxOf { it.id } + 1
                            notes.add(Note(id, title, content))
                        } else {
                            editNote?.title = title
                            editNote?.content = content
                        }
                        saveNotes(context, notes)
                        showDialog = false
                    }
                )
            }
        }
    }
}

@Composable
fun NotesList(
    notes: List<Note>,
    onEdit: (Note) -> Unit,
    onDelete: (Note) -> Unit
) {
    LazyColumn(modifier = Modifier.fillMaxSize().padding(8.dp)) {
        items(notes) { note ->
            Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 4.dp)
                    .clickable { onEdit(note) },
                elevation = CardDefaults.cardElevation(defaultElevation = 4.dp)
            ) {
                Column(modifier = Modifier.padding(12.dp)) {
                    Text(text = note.title, fontSize = 18.sp)
                    Spacer(modifier = Modifier.height(4.dp))
                    Text(text = note.content, fontSize = 14.sp)
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(
                        text = "Удалить",
                        color = Color.Red,
                        modifier = Modifier.clickable { onDelete(note) }
                    )
                }
            }
        }
    }
}

@Composable
fun AddEditNoteDialog(
    note: Note?,
    onDismiss: () -> Unit,
    onSave: (String, String) -> Unit
) {
    var title by remember { mutableStateOf(note?.title ?: "") }
    var content by remember { mutableStateOf(note?.content ?: "") }

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text(if (note == null) "Добавить заметку" else "Редактировать заметку") },
        text = {
            Column {
                BasicTextField(
                    value = title,
                    onValueChange = { title = it },
                    decorationBox = { inner ->
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .background(Color.LightGray)
                                .padding(4.dp)
                        ) { inner() }
                    }
                )
                Spacer(modifier = Modifier.height(8.dp))
                BasicTextField(
                    value = content,
                    onValueChange = { content = it },
                    decorationBox = { inner ->
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(150.dp)
                                .background(Color(0xFFEFEFEF))
                                .padding(4.dp)
                        ) { inner() }
                    }
                )
            }
        },
        confirmButton = {
            TextButton(onClick = { onSave(title, content) }) { Text("Сохранить") }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) { Text("Отмена") }
        }
    )
}
