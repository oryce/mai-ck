'use client'

import clsx from 'clsx'
import { useSession } from 'next-auth/react'
import { useEffect, useRef, useState } from 'react'

import { uploadDocument } from '@/api/documents'
import { getTaskStatus } from '@/api/task'
import { Heading } from '@/components/heading'
import { Strong, Text } from '@/components/text'
import { DocumentArrowUpIcon } from '@heroicons/react/24/outline'

function UploadForm({ setFiles }) {
  const fileInput = useRef(null)

  const handleSelect = (e) => {
    e.preventDefault()
    setFiles(Array.from(e.target.files))
  }

  const handleDrop = (e) => {
    e.preventDefault()

    const droppedFiles = e.dataTransfer.files

    if (droppedFiles.length > 0) {
      setFiles(Array.from(droppedFiles))
    }
  }

  return (
    <div className="flex size-full items-center justify-center">
      <div
        className={clsx(
          'flex h-[350px] w-[550px] cursor-pointer flex-col items-center justify-center',
          'rounded-2xl bg-gray-50/50 p-16 shadow-lg ring-1 ring-gray-200'
        )}
        onClick={() => fileInput.current.click()}
        onDrop={handleDrop}
        onDragOver={(e) => e.preventDefault()}
      >
        <DocumentArrowUpIcon className="h-28 w-28 text-neutral-800" />
        <Text className="mt-4 text-center !text-base !text-neutral-800">
          Перетащите сюда документы, или нажмите, чтобы выбрать файлы
        </Text>
        <Text className="mt-2">Максимальный размер документа: 100 Мб</Text>
        <input
          ref={fileInput}
          className="hidden"
          type="file"
          multiple
          onChange={handleSelect}
        />
      </div>
    </div>
  )
}

function UploadingFile({ file }) {
  const { data: session } = useSession()

  const [status, setStatus] = useState('uploading')
  const [progress, setProgress] = useState(0)
  const [taskId, setTaskId] = useState(null)
  const [fetchInterval, setFetchInterval] = useState(-1)

  const translateStatus = (status) => {
    return {
      uploading: 'Загрузка...',
      preprocessing: 'Оцифровка...',
      processing: 'Обработка...',
      finished: 'Загружено',
      error: 'Ошибка загрузки',
    }[status]
  }

  const updateTaskStatus = () => {
    getTaskStatus({ session, taskId })
      .then(({ status, progress }) => {
        setStatus(status)
        setProgress(progress)
      })
      .catch((err) => {
        console.error('Task status fetch failed', err)
        setStatus('error')
      })
  }

  useEffect(() => {
    uploadDocument({
      session,
      file,
      uploadCb: (progress) =>
        setProgress(progress === -1 ? -1 : Math.ceil(progress * 100)),
    })
      .then((res) => setTaskId(res.taskId))
      .catch((err) => {
        console.error('Upload failed', err)
        setStatus('error')
      })
  }, [])

  useEffect(() => {
    if (!taskId) return
    setFetchInterval(setInterval(updateTaskStatus, 2500))
  }, [taskId])

  useEffect(() => {
    if (status === 'finished' || status === 'error') {
      clearInterval(fetchInterval)
      setFetchInterval(-1)
    }
  }, [status])

  return (
    <div
      className={clsx(
        'relative rounded-md md:w-[240px]',
        'shadow-xs ring-1 ring-zinc-950/5 dark:ring-white/10'
      )}
    >
      <div
        className={clsx(
          'h-[300px] rounded-t-md',
          'bg-[url(/pdf-placeholder.jpg)] bg-cover bg-center'
        )}
        role="presentation"
      />
      <div className="p-2">
        <Text className="!text-base">
          <Strong>{file.name}</Strong>
        </Text>
        <span className="mt-1.5 flex justify-between">
          <Text>{translateStatus(status)}</Text>
          {status != 'error' && <Text>{progress}%</Text>}
        </span>
        {status != 'error' && (
          <div className="relative mt-0.5 h-1.5 w-full rounded-full bg-neutral-200">
            <div
              className="absolute h-full rounded-full bg-blue-500"
              style={{ width: `${progress}%` }}
            />
          </div>
        )}
      </div>
    </div>
  )
}

function UploadStatus({ files }) {
  return (
    <div className="mt-4 grid grid-cols-4 gap-4">
      {files.map((file, i) => (
        <UploadingFile key={i} file={file} />
      ))}
    </div>
  )
}

export default function Upload() {
  const [files, setFiles] = useState([])

  return (
    <div className="h-full">
      <Heading>Загрузка документов</Heading>
      {files.length > 0 ? (
        <UploadStatus files={files} />
      ) : (
        <UploadForm setFiles={setFiles} />
      )}
    </div>
  )
}
