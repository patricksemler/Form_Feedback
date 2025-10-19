import { Picker } from '@react-native-picker/picker';
import * as ImagePicker from 'expo-image-picker';
import { useState } from 'react';
import { Dimensions, StyleSheet, Text, TouchableOpacity, View } from 'react-native';

const { height, width } = Dimensions.get('window');

const buttonHeight = height * 0.07;
const buttonWidth = width * 0.6;

export default function HomeScreen() {
    const [videoURI, setVideoURI] = useState<string | null>(null);
    const [uploading, setUploading] = useState(false);

    enum Exercise {
        PUSHUP = 'pushup',
        SITUP = 'situp',
        SQUAT = 'squat',
        LUNGE = 'lunge',
    };

    const [selectedExercise, setSelectedExercise] = useState(Exercise.PUSHUP);

    async function pickAndUploadVideo() {
        const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();

        if (status !== 'granted') {
            alert('Media library permissions not granted.');
            return;
        }

        const result = await ImagePicker.launchImageLibraryAsync({
            mediaTypes: ImagePicker.MediaTypeOptions.Videos,
            allowsEditing: false,
            quality: 0.5,
        });

        if (result.canceled || !result.assets || result.assets.length === 0) {
            return;
        }

        const pickedURI = result.assets[0].uri;
        setVideoURI(pickedURI);
        console.log('Picked video URI:', pickedURI);

        const formData = new FormData();

        formData.append('exercise', selectedExercise);
        formData.append('video', {
            uri: pickedURI,
            name: `${Date.now()}.mp4`,
            type: 'video/mp4',
        } as any);

        setUploading(true);

        try {
            const response = await fetch('http://10.246.79.39:5001/analyze', {
                method: 'POST',
                body: formData,
            });

            const json = await response.json().catch(() => null);

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(errorText);
            }

            alert('Upload succeeded!');
        } catch (error) {
            console.error('Error:', error);
            alert('Upload failed.')
        } finally {
            setUploading(false);
            console.log('Upload finished (success or error).');
        }
    }

    return (
        <View style={styles.container}>
            <Text style={styles.title}>Form Feedback</Text>

            <View style={styles.pickerContainer}>
                <Picker
                    selectedValue={selectedExercise}
                    onValueChange={(itemValue) => {
                        setSelectedExercise(itemValue as Exercise);
                    }}
                    style={styles.picker}
                >
                    <Picker.Item label='Push Up' value={Exercise.PUSHUP} />
                    <Picker.Item label='Sit Up' value={Exercise.SITUP} />
                    <Picker.Item label='Squat' value={Exercise.SQUAT} />
                    <Picker.Item label='Lunge' value={Exercise.LUNGE} />
                </Picker>
            </View>

            <TouchableOpacity style={styles.button} onPress={pickAndUploadVideo}>
                <Text>Upload Video</Text>
            </TouchableOpacity>
            {videoURI && (
                <Text style={styles.paragraph}>Selected video: {videoURI}</Text>
            )}
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    },
    title: {
        fontSize: 24,
        fontWeight: 'bold',
        marginBottom: 10,
        color: '#000',
    },
    paragraph: {
        fontSize: 18,
        marginBottom: 10,
        color: '#000',
    },
    button: {
        width: buttonWidth,
        height: buttonHeight,
        backgroundColor: '#1E90FF',
        borderRadius: 8,
        alignItems: 'center',
        justifyContent: 'center',
        marginBottom: 20,
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.3,
    },
    picker: {
        color: '#000',
        paddingHorizontal: 10,
    },
    pickerContainer: {
        width: buttonWidth,
        height: buttonHeight,
        backgroundColor: '#1E90FF',
        borderRadius: 8,
        justifyContent: 'center',
        marginBottom: 20,
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.3,
        overflow: 'hidden',
    },
});