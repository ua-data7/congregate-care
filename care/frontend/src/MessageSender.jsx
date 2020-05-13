import React from 'react';

import {
    Typography, Grid, Box, FormControl,
    Paper, TextField, Toolbar, Button
} from '@material-ui/core';

export default function MessageSender({selected}) {

    if (selected.length === 0) return null;

    return (
        <Paper>
        
            <Toolbar>
                <Typography variant="h6" component="h2">
                    Send messages to {selected.length} {selected.length > 1 ? 'facilities' : 'facility'}
                </Typography>
            </Toolbar>
            <Box p={3}>
                <Grid container spacing={3}>
                    <Grid item xs={3}>
                        <Typography variant="subtitle1" component="h3">SMS</Typography>
                        <FormControl fullWidth>
                            <TextField
                                placeholder="Enter message"
                                multiline
                                rows={5}
                            />
                        </FormControl>
                    </Grid>
                    <Grid item xs={5}>
                        <Typography variant="subtitle1" component="h3">Email</Typography>
                        <FormControl fullWidth>
                            <TextField
                                placeholder="Enter message"
                                multiline
                                rows={5}
                            />
                        </FormControl>
                    </Grid>
                    <Grid item xs={12}>
                        <Button variant="contained" color="primary">Send</Button>
                    </Grid>
                </Grid>
            </Box>
        </Paper>
    );
}
