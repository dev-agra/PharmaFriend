const APP_ID = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx';
const APP_CERT = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx';
// generate this token after every 24hrs
const APP_TOKEN = sessionStorage.getItem('token');
const APP_CHANNEL = sessionStorage.getItem('room_name');
let UID = sessionStorage.getItem('UID');
const client = AgoraRTC.createClient({mode:'rtc', codec: 'vp8' })
let localTracks = []
let remoteUsers = {}

let joinAndDisplayLocalStream = async () => {
    document.getElementById('room-name').innerText = APP_CHANNEL
    client.on('user-published', handleUserJoined)
    client.on('user-left', handleUserLeft)

    try{
        await client.join(APP_ID, APP_CHANNEL, APP_TOKEN, UID)
    }catch(error){
        console.error(error)
        window.open('/', '_self')
    }

    
    // 0 for audio and 1 for video below
    localTracks = await AgoraRTC.createMicrophoneAndCameraTracks()
    

    let player = `<div class="video-container" id="user-container-${UID}">
                    <div><span class="user">My Name</span></div>
                    <div class="video-player" id="user-${UID}"></div>
                </div>`
    document.getElementById('video-streams').insertAdjacentHTML ('beforeend', player)

    localTracks[1].play(`user-${UID}`)
    await client.publish([localTracks[0], localTracks[1]])
}

let handleUserJoined = async (user, mediaType) => {
    remoteUsers[user.uid] = user
    await client.subscribe(user, mediaType)
    if(mediaType === 'video'){
        let player = document.getElementById(`user-container-${user.uid}`)
        
        if(player != null){
            player.remove()
        }

        player =`<div class="video-container" id="user-container-${user.uid}">
                    <div><span class="user">My Name</span></div>
                    <div class="video-player" id="user-${user.uid}"></div>
                </div>`
        document.getElementById('video-streams').insertAdjacentHTML ('beforeend', player)
        user.videoTrack.play(`user-${user.uid}`)
    }

    if(mediaType === 'audio') {
        user.audioTrack.play()
    }
}

let handleUserLeft = async (user) => {
    delete remoteUsers[user.uid]
    document.getElementById(`user-container-${user.uid}`).remove()
}

let leaveAndRemoveLocalStream = async () => {
    for(let i = 0; localTracks.length > i; i++){
        localTracks[i].stop()
        localTracks[i].close()
    }

    await client.leave()
    window.open('/', '_self')
} 

let toggleCamera = async (e) => {
    if (localTracks[1].muted){
        await localTracks[1].setMuted(false)
        e.target.style.backgroundColor = '#fff'
    }
    else{
        await localTracks[1].setMuted(true)
        e.target.style.backgroundColor = 'rgb(255, 80, 80, 1)'
    }
}

let toggleMic = async (e) => {
    if (localTracks[0].muted){
        await localTracks[0].setMuted(false)
        e.target.style.backgroundColor = '#fff'
    }
    else{
        await localTracks[0].setMuted(true)
        e.target.style.backgroundColor = 'rgb(255, 80, 80, 1)'
    }
}

joinAndDisplayLocalStream()
document.getElementById('leave-btn').addEventListener('click', leaveAndRemoveLocalStream)
document.getElementById('vid-btn').addEventListener('click', toggleCamera)
document.getElementById('mic-btn').addEventListener('click', toggleMic)
