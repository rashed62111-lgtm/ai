-- Create messages table
CREATE TABLE IF NOT EXISTS messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    role TEXT NOT NULL, -- 'user' or 'ai'
    content TEXT NOT NULL
);

-- Enable row level security (optional but recommended)
-- ALTER TABLE messages ENABLE ROW LEVEL SECURITY;
