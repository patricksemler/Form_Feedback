import * as ImagePicker from 'expo-image-picker';
import { useState } from 'react';
import { Dimensions, StyleSheet, Text, TouchableOpacity, View } from 'react-native';

const deviceHeight = Dimensions.get('window').height;
const deviceWidth = Dimensions.get('window').width;
const deviceMinDimension = Math.min(deviceWidth, deviceHeight);

const serverIP = '10.246.79.39';
const serverPort = '5001';

enum Exercise {
    PUSHUP = 'Push Up',
    SITUP = 'Sit Up',
    SQUAT = 'Squat',
    LUNGE = 'Lunge',
};

const exerciseOrder = [
    Exercise.PUSHUP,
    Exercise.SITUP,
    Exercise.SQUAT,
    Exercise.LUNGE
];

export default function HomeScreen() {
    const [videoURI, setVideoURI] = useState<string | null>(null);
    const [selectedExercise, setSelectedExercise] = useState(Exercise.PUSHUP);

    function cycleExercise() {
        const currentIndex = exerciseOrder.indexOf(selectedExercise);
        const newIndex = (currentIndex + 1) % exerciseOrder.length;

        setSelectedExercise(exerciseOrder[newIndex]);
        console.log(`[Exercise] Switched exerciseOrder index from ${currentIndex} to ${newIndex}.`)
    }

    async function pickAndUploadVideo() {
        console.log(`[Upload] Requesting media library permissions.`)
        const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();

        if (status !== 'granted') {
            console.log(`[Upload] Media library permissions not granted.`)
            return;
        }
        console.log(`[Upload] Media library permissions granted.`)

        console.log(`[Upload] Getting video from user.`)
        const result = await ImagePicker.launchImageLibraryAsync({
            mediaTypes: ImagePicker.MediaTypeOptions.Videos,
            allowsEditing: false,
            quality: 0.5,
        });

        if (result.canceled || !result.assets || result.assets.length === 0) {
            return;
        }
        console.log(`[Upload] Video received.`)

        const pickedURI = result.assets[0].uri;
        setVideoURI(pickedURI);
        console.log(`[Upload] Picked video URI: ${pickedURI}.`);

        console.log(`[Upload] Creating form data.`);
        const formData = new FormData();
        formData.append('exercise', selectedExercise);
        formData.append('video', {
            uri: pickedURI,
            name: `${Date.now()}.mp4`,
            type: 'video/mp4',
        } as any);
        console.log(`[Upload] Form data created.`);

        try {
            console.log(`[Upload] Beginning upload.`);
            const response = await fetch(`http://${serverIP}:${serverPort}/analyze`, {
                method: 'POST',
                body: formData,
            });

            const json = await response.json().catch(() => null);

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(errorText);
            }
            console.log(`[Upload] Upload succeeded.`)
        } catch (error) {
            console.error(`[Upload] Upload failed. Error: {error}`);
        }
    }

    return (
        <View style={styles.container}>
            <Text style={styles.title}>Form Feedback</Text>

            <View style={styles.gap}></View>

            <TouchableOpacity style={styles.button} onPress={cycleExercise}>
                <Text style={styles.buttonText}>{selectedExercise}</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.button} onPress={pickAndUploadVideo}>
                <Text style={styles.buttonText}>Upload Video</Text>
            </TouchableOpacity>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        flexDirection: 'column',
        backgroundColor: '#FFF',
    },
    gap: {
        flex: 4 / 5,
    },
    title: {
        fontSize: deviceMinDimension * 0.08,
        fontWeight: 'bold',
        color: '#000',
    },
    button: {
        width: deviceWidth * 0.75,
        height: deviceHeight * 0.08,
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: '#222',
        borderRadius: 8,
        marginTop: 10,
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.3,
    },
    buttonText: {
        fontSize: deviceWidth * 0.042,
        fontWeight: 'bold',
        color: '#FFFFFF',
    },
});