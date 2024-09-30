import React, { useState } from 'react';

export interface FileItem {
    name: string;
    type: 'file' | 'folder';
    children?: FileItem[];
}

interface FileExplorerProps {
    items: FileItem[];
}

const FileExplorer: React.FC<FileExplorerProps> = ({ items }) => {
    const [openFolders, setOpenFolders] = useState<Set<string>>(new Set());

    const toggleFolder = (folderName: string) => {
        const updatedFolders = new Set(openFolders);
        if (updatedFolders.has(folderName)) {
            updatedFolders.delete(folderName);
        } else {
            updatedFolders.add(folderName);
        }
        setOpenFolders(updatedFolders);
    };

    const renderItems = (items: FileItem[]) => {
        return (
            <ul>
                {items.map((item) => (
                    <li key={item.name}>
                        {item.type === 'folder' ? (
                            <span onClick={() => toggleFolder(item.name)} style={{ cursor: 'pointer' }}>
                                {openFolders.has(item.name) ? '📂' : '📁'} {item.name}
                            </span>
                        ) : (
                            <span>
                                📄 {item.name}
                            </span>
                        )}
                        {item.type === 'folder' && openFolders.has(item.name) && item.children && (
                            <div style={{ paddingLeft: '20px' }}>
                                {renderItems(item.children)}
                            </div>
                        )}
                    </li>
                ))}
            </ul>
        );
    };

    return <div>{renderItems(items)}</div>;
};

export default FileExplorer;
