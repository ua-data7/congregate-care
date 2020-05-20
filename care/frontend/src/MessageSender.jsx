import React from 'react';
import axios from 'axios';

import {
    Typography, Grid, Box, FormControl,
    Paper, TextField, Toolbar, Button
} from '@material-ui/core';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

export default function MessageSender({recipients, closeModal}) {

    const [email, setEmail] = React.useState('');
    const [sms, setSms] = React.useState('');
    const [subject, setSubject] = React.useState('');
        
    const [copied, setCopied] = React.useState(false);
    function copyEmails() {
        let emails = recipients.map(facility => facility.emails).join(',');
        navigator.clipboard.writeText(emails);
        setCopied(true);
    }
    React.useEffect(() => {
        setCopied(false);
    }, [recipients]);

    function send() {
        let uuids = recipients.map(r => r.identity);
        axios.post('/api/sendemail', {
            uuid: uuids,
            bulk: true,
            subject: subject,
            message: email
        });

        axios.post('/api/sendsms', {
            uuid: uuids,
            bulk: true,
            message: sms
        });
        closeModal();
    }

    return (
        <Paper>
            <Toolbar spacing={3}>
                <Typography variant="h6" component="h2" style={{flexGrow: 1}}>
                    Send messages to {recipients.length} {recipients.length > 1 ? 'facilities' : 'facility'}
                </Typography>
                <Button variant="contained" color="secondary" onClick={copyEmails}>
                    { copied ? 'Copied!' : 'Copy Email Addresses'}
                </Button>
            </Toolbar>
            <Box p={3}>
                <Grid container spacing={3}>
                    <Grid item xs={6}>
                        <Typography variant="subtitle1" component="h3">Email</Typography>
                        <FormControl fullWidth>
                            <TextField
                                value={subject}
                                onChange={event => setSubject(event.target.value)}
                                placeholder="Subject"
                            />
                            <TextField
                                value={email}
                                onChange={event => setEmail(event.target.value)}
                                placeholder="Body"
                                multiline
                                rows={4}
                            />
                        </FormControl>
                    </Grid>
                    <Grid item xs={5}>
                        <Typography variant="subtitle1" component="h3">SMS (Optional)</Typography>
                        <FormControl fullWidth>
                            <TextField
                                value={sms}
                                onChange={event => setSms(event.target.value)}
                                placeholder="Enter message (160 chars max)"
                                multiline
                                rows={5}
                            />
                        </FormControl>
                    </Grid>
                    <Grid item xs={12}>
                        <Button variant="contained" color="primary"  disabled={!subject || !email} onClick={send}>Send</Button>
                        <Button style={{marginLeft: '5px'}} onClick={closeModal}>Close</Button>
                    </Grid>
                </Grid>
            </Box>
        </Paper>
    );
}
